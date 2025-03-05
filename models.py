from dataclasses import dataclass
from datetime import datetime

@dataclass
class Position:
    symbol: str
    entry_price: float
    leverage: int
    position_side: str
    break_even_price: float
    position_amount: float
    mark_price: float = None
    created_at: datetime = None

    @classmethod
    def from_api_data(cls, data: dict):
        return cls(
            symbol=data['symbol'],
            entry_price=float(data['entryPrice']),
            leverage=int(data['leverage']),
            position_side=data['positionSide'],
            break_even_price=float(data['breakEvenPrice']),
            position_amount=float(data['positionAmount']),
            mark_price=float(data['markPrice']) if 'markPrice' in data else None,
            created_at=datetime.now()
        )

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'entry_price': self.entry_price,
            'leverage': self.leverage,
            'position_side': self.position_side,
            'break_even_price': self.break_even_price,
            'position_amount': self.position_amount,
            'mark_price': self.mark_price,
            'created_at': self.created_at
        }
