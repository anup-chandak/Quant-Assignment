
import os, json
import random
import openai  # type: ignore
from dotenv import load_dotenv  # type: ignore
from strategies.base import Strategy

class LLMStrategy(Strategy):
    def __init__(self,
                 model="gpt-3.5-turbo",
                 temperature=0.7,
                 max_tokens=50,
                 fallback_buy_rate=0.5,
                 fallback_sell_rate=0.9,
                 vol_range=(1,5)):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.buy_rate = fallback_buy_rate
        self.sell_rate = fallback_sell_rate
        self.vol_min, self.vol_max = vol_range

    def decide(self, trader_id, tick, price):
        prompt = (
            f"You are trader #{trader_id} on tick {tick}. "
            f"Market price is {price:.2f}. "
            "Respond _only_ with a JSON object: "
            "{\"action\":\"buy\"|\"sell\"|\"hold\",\"volume\":<int>}."
        )
        sys_msg = {"role": "system", "content": "You are a trading agent."}
        usr_msg = {"role": "user", "content": prompt}

        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[sys_msg, usr_msg],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            text = resp.choices[0].message.content.strip()
            decision = json.loads(text)
            source = "LLM"
        except Exception:
            decision = self._fallback()
            source = "FALLBACK"

        print(f"[LLM:{source}] trader={trader_id} tick={tick} → {decision}")
        return decision

    def _fallback(self):
        r = random.random()
        if r < self.buy_rate:
            return {"action": "buy", "volume": random.randint(self.vol_min, self.vol_max)}
        elif r < self.sell_rate:
            return {"action": "sell", "volume": random.randint(self.vol_min, self.vol_max)}
        else:
            return {"action": "hold", "volume": 0}
