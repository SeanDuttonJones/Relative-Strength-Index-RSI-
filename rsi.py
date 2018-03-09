class RSI(object):

    def __init__(self, OHLC, period):
        self.OHLC = OHLC
        self.period = period
        self.gain_loss = self.gain_loss_calc()

    def gain_loss_calc(self):
        data = self.OHLC["close"]
        gain_loss = []

        for i in range(1, len(data)):
            change = float(data[i]) - float(data[i-1])
            if change >= 0:
                gain_loss.append({"gain": change, "loss": 0})
            else:
                gain_loss.append({"gain": 0, "loss": abs(change)})

        return gain_loss

    def first_avg_calc(self):
        gain_loss = self.gain_loss
        gain = 0
        loss = 0

        for i in range(0, self.period):
            gain += gain_loss[i]["gain"]
            loss += gain_loss[i]["loss"]

        gain = gain / self.period
        loss = loss / self.period

        return {"gain": gain, "loss": loss}

    def rsi_calc(self):
        gain_loss = self.gain_loss
        prev_avg_gain_loss = self.first_avg_calc()
        avg_gain = 0
        avg_loss = 0

        for i in range(self.period, len(gain_loss)):
            avg_gain = ((prev_avg_gain_loss["gain"] * (self.period - 1)) + gain_loss[i]["gain"]) / self.period
            prev_avg_gain_loss["gain"] = avg_gain

            avg_loss = ((prev_avg_gain_loss["loss"] * (self.period - 1)) + gain_loss[i]["loss"]) / self.period
            prev_avg_gain_loss["loss"] = avg_loss

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi
