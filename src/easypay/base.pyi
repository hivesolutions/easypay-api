from typing import Any, Dict, List, NotRequired, Optional, Mapping, Sequence, TypedDict
from threading import Thread
from appier import API
from xml.dom.minidom import Node

from .mb import MBAPI
from .payment import PaymentAPI

LOOP_TIMEOUT: float = ...
BASE_URL: str = ...
BASE_URL_TEST: str = ...
BASE_URL_V2: str = ...
BASE_URL_TEST_V2: str = ...

class Reference(TypedDict):
    cin: str
    username: str
    entity: str
    reference: str
    value: str
    identifier: str
    warning: float | None
    cancel: float | None
    status: str

class Doc(TypedDict):
    cin: str
    username: str
    identifier: str
    key: str

class Payment(TypedDict):
    amount: float
    currency: str
    method: str
    type: NotRequired[str | None]
    key: str
    capture: NotRequired[Dict[str, Any]]
    customer: NotRequired[Dict[str, Any]]
    warning: float | None
    cancel: float | None
    status: str
    identifier: str

class Scheduler(Thread):
    def __init__(
        self,
        api: ...,
        loop_timeout: float = ...,
        tick_docs: bool = ...,
        tick_references: bool = ...,
        tick_payments: bool = ...,
    ) -> None: ...
    def run(self) -> None: ...
    def stop(self) -> None: ...
    def tick(self) -> None: ...
    def _tick_docs(self) -> None: ...
    def _tick_references(self) -> None: ...
    def _tick_payments(self) -> None: ...

class API(API, MBAPI):
    def __init__(self, *args, **kwargs) -> None: ...
    @classmethod
    def cleanup(cls, *args, **kwargs) -> None: ...
    def destroy(self) -> None: ...
    def start_scheduler(self) -> None: ...
    def stop_scheduler(self) -> None: ...
    def diagnostics(self) -> Mapping[str, Any]: ...
    def gen_reference(
        self,
        data: Mapping[str, Any],
        warning: float | None = ...,
        cancel: float | None = ...,
    ) -> Reference: ...
    def gen_doc(self, identifier: str, key: str) -> Doc: ...
    def new_reference(self, reference: Reference) -> None: ...
    def set_reference(self, reference: Reference) -> None: ...
    def del_reference(self, identifier: str) -> None: ...
    def list_references(self) -> Sequence[Reference]: ...
    def get_reference(self, identifier: str) -> Reference | None: ...
    def new_doc(self, doc: Doc) -> None: ...
    def del_doc(self, identifier: str) -> None: ...
    def list_docs(self) -> Sequence[Doc]: ...
    def get_doc(self, identifier: str) -> Doc | None: ...
    def next(self) -> int: ...
    def generate(self) -> str: ...
    def validate(self, cin: str | None = -..., username: str | None = ...) -> None: ...
    def loads(self, data: str) -> Dict[str, Any]: ...
    def dumps(
        self, map: Dict[str, Any], root: str = ..., encoding: str = ...
    ) -> bytes: ...
    def _text(self, node: Node) -> str | None: ...

class ShelveAPI(API):
    def __init__(self, *args, **kwargs) -> None: ...

class APIv2(API, PaymentAPI):
    def __init__(self, *args, **kwargs) -> None: ...
    @classmethod
    def cleanup(cls, *args, **kwargs) -> None: ...
    def destroy(self) -> None: ...
    def start_scheduler(self) -> None: ...
    def stop_scheduler(self) -> None: ...
    def diagnostics(self) -> Mapping[str, Any]: ...
    def set_payment(self, payment: Payment) -> None: ...
    def del_payment(self, identifier: str) -> None: ...
    def list_payments(self) -> Sequence[Payment]: ...
    def get_payment(self, identifier: str) -> Payment | None: ...

class ShelveAPIv2(APIv2):
    def __init__(self, *args, **kwargs) -> None: ...
