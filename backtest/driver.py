"""Bar replay driver: feeds per-TF bar series through MTFEngine in strict
timestamp order (descending TF at shared closes is enforced inside
MTFEngine.process). Used by the perturbation test now; the real backtest
loop builds on the same replay discipline with the ClockGatedFeed."""


def replay(engine, minute_bars, signal_every=15, context_every=60,
           make_bar=None):
    """minute_bars: list of Bar (execution TF, close-ts = Bar.ts, 1..n).
    Signal/context bars are aggregates of the minutes they span, closing at
    multiples of signal_every/context_every. make_bar(ts, bars, tf) builds
    an aggregate bar."""
    buf_sig, buf_ctx = [], []
    for b in minute_bars:
        buf_sig.append(b)
        buf_ctx.append(b)
        sig = ctx = None
        if b.ts % signal_every == 0:
            sig = make_bar(b.ts, buf_sig, "15min")
            buf_sig = []
        if b.ts % context_every == 0:
            ctx = make_bar(b.ts, buf_ctx, "1h")
            buf_ctx = []
        engine.process(b.ts, context_bar=ctx, signal_bar=sig, exec_bar=b)
