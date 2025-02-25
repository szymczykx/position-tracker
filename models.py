from dataclasses import dataclass
from datetime import datetime

@dataclass
class Position:
    symbol: str
    entry_price: float
    leverage: int
    position_side: str
    break_even_price: float
    adl: int
    created_at: datetime = None

    @classmethod
    def from_api_data(cls, data: dict):
        return cls(
            symbol=data['symbol'],
            entry_price=float(data['entryPrice']),
            leverage=int(data['leverage']),
            position_side=data['positionSide'],
            break_even_price=float(data['breakEvenPrice']),
            adl=int(data['adl']),
            created_at=datetime.now()
        )

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'entry_price': self.entry_price,
            'leverage': self.leverage,
            'position_side': self.position_side,
            'break_even_price': self.break_even_price,
            'adl': self.adl,
            'created_at': self.created_at
        }
