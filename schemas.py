from pydantic import BaseModel


class BMDTransactionRequest(BaseModel):
    sender: str
    recipient: str
    amount: int


class BMDNodesRequest(BaseModel):
    nodes: list[str]
