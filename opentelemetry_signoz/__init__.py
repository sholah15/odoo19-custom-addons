import time
import logging
import odoo
from odoo.tools import config
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
try:
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
except ImportError:
    RequestsInstrumentor = None

try:
    from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
except ImportError:
    Psycopg2Instrumentor = None

_logger = logging.getLogger(__name__)

_INITIALIZED = False


def _get_config(name, default=None):
    return config.get(name, default)


def init_tracer():
    global _INITIALIZED
    if _INITIALIZED:
        return
    service_name = _get_config(
        "otel_service_name",
        "odoo"
    )
    traces_endpoint = _get_config(
        "otel_exporter_otlp_traces_endpoint",
        "http://172.17.0.1:4318/v1/traces"
    )
    protocol = _get_config(
        "otel_exporter_otlp_protocol",
        "http/protobuf"
    )
    exporter_name = _get_config(
        "otel_traces_exporter",
        "otlp"
    )
    if exporter_name != "otlp":
        _logger.warning(
            "Unsupported exporter %s",
            exporter_name
        )
        return
    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": odoo.release.version,
        }
    )
    provider = TracerProvider(
        resource=resource
    )
    exporter = OTLPSpanExporter(
        endpoint=traces_endpoint
    )
    provider.add_span_processor(
        BatchSpanProcessor(exporter)
    )
    trace.set_tracer_provider(provider)
    _INITIALIZED = True
    _logger.info(
        "OpenTelemetry initialized "
        "service=%s endpoint=%s protocol=%s",
        service_name,
        traces_endpoint,
        protocol,
    )
    if RequestsInstrumentor is not None:
        RequestsInstrumentor().instrument()
    else:
        _logger.warning("opentelemetry-instrumentation-requests not installed, skipping.")
    if Psycopg2Instrumentor is not None:
        Psycopg2Instrumentor().instrument()
    else:
        _logger.warning("opentelemetry-instrumentation-psycopg2 not installed, skipping.")


def _patch_dispatcher(dispatcher_cls):
    tracer = trace.get_tracer("odoo.http")
    original = dispatcher_cls.dispatch
    if getattr(dispatcher_cls, "_otel_patched", False):
        return
    def dispatch(self, endpoint, args):
        path = "/"
        try:
            from odoo.http import request
            if request and request.httprequest:
                path = request.httprequest.path
        except Exception:
            pass
        with tracer.start_as_current_span(path) as span:
            span.set_attribute(
                "odoo.dispatcher",
                dispatcher_cls.__name__,
            )
            span.set_attribute(
                "odoo.endpoint",
                getattr(
                    endpoint,
                    "__name__",
                    str(endpoint),
                ),
            )
            return original(
                self,
                endpoint,
                args,
            )
    dispatcher_cls.dispatch = dispatch
    dispatcher_cls._otel_patched = True


def patch_http():
    import odoo.http
    _patch_dispatcher(
        odoo.http.HttpDispatcher
    )
    _patch_dispatcher(
        odoo.http.JsonRPCDispatcher
    )
    if hasattr(
        odoo.http,
        "Json2Dispatcher"
    ):
        _patch_dispatcher(
            odoo.http.Json2Dispatcher
        )
    _logger.info(
        "SigNoz HTTP tracing enabled"
    )


def patch_cron():
    from odoo.addons.base.models.ir_cron import IrCron
    tracer = trace.get_tracer("odoo.cron")
    original = IrCron._callback
    if getattr(
        IrCron,
        "_otel_patched",
        False
    ):
        return
    def callback(
        self,
        cron_name,
        server_action_id,
    ):
        with tracer.start_as_current_span(
            f"cron.{cron_name}"
        ):
            return original(
                self,
                cron_name,
                server_action_id,
            )
    IrCron._callback = callback
    IrCron._otel_patched = True
    _logger.info(
        "SigNoz cron tracing enabled"
    )


def patch_sql():
    from odoo.sql_db import Cursor
    tracer = trace.get_tracer("odoo.sql")
    slow_ms = int(
        config.get(
            "otel_sql_slow_ms",
            500,
        )
    )
    if getattr(Cursor, "_otel_patched", False):
        _logger.info("SigNoz SQL tracing already enabled")
        return
    original_execute = Cursor.execute
    def execute(
        self,
        query,
        params=None,
        log_exceptions=True,
    ):
        start = time.perf_counter()
        try:
            result = original_execute(
                self,
                query,
                params=params,
                log_exceptions=log_exceptions,
            )
            elapsed_ms = (
                time.perf_counter() - start
            ) * 1000
            # hanya trace query lambat
            if elapsed_ms >= slow_ms:
                with tracer.start_as_current_span(
                    "sql.slow"
                ) as span:
                    span.set_attribute(
                        "db.system",
                        "postgresql",
                    )
                    span.set_attribute(
                        "db.operation",
                        query.split(None, 1)[0].upper()
                        if query else "UNKNOWN",
                    )
                    span.set_attribute(
                        "db.duration_ms",
                        round(elapsed_ms, 2),
                    )
                    span.set_attribute(
                        "db.statement",
                        query[:4000],
                    )
                    span.set_attribute(
                        "db.params_count",
                        len(params) if params else 0,
                    )
            return result
        except Exception as exc:
            elapsed_ms = (
                time.perf_counter() - start
            ) * 1000
            with tracer.start_as_current_span(
                "sql.error"
            ) as span:
                span.set_attribute(
                    "db.system",
                    "postgresql",
                )
                span.set_attribute(
                    "db.duration_ms",
                    round(elapsed_ms, 2),
                )
                span.set_attribute(
                    "db.statement",
                    query[:4000] if query else "",
                )
                span.set_attribute(
                    "error",
                    True,
                )
                span.set_attribute(
                    "exception.type",
                    exc.__class__.__name__,
                )
                span.set_attribute(
                    "exception.message",
                    str(exc),
                )
            raise
    Cursor.execute = execute
    Cursor._otel_patched = True
    _logger.info(
        "SigNoz slow SQL tracing enabled, treshold = %s",
        slow_ms
    )


def make_wrapper(original, method_name):
    tracer = trace.get_tracer("odoo.orm")
    def wrapper(
        self,
        *args,
        **kwargs
    ):
        with tracer.start_as_current_span(
            f"{self._name}.{method_name}"
        ):
            return original(
                self,
                *args,
                **kwargs
            )
    return wrapper


def patch_orm():
    from odoo.models import BaseModel
    methods = [
        "search",
        "read",
        "write",
        "create",
        "unlink",
    ]
    for method_name in methods:
        original = getattr(
            BaseModel,
            method_name
        )
        setattr(
            BaseModel,
            method_name,
            make_wrapper(
                original,
                method_name
            )
        )
    _logger.info(
        "SigNoz ORM tracing enabled"
    )


def post_load():
    init_tracer()
    patch_http()
    patch_cron()
    patch_sql()
    patch_orm()
