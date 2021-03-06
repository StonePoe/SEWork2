import talib
from rqalpha.api import history, plot, order_target_value, order_shares, update_universe


def init(context):
    # context.s1 = "000001.XSHE"
    context.s1 = "000001.XSHE"
    context.s2 = "601988.XSHG"
    context.s3 = "000068.XSHE"
    context.stocks = [context.s1,context.s2,context.s3]
    # context.stocks = ["000001.XSHE", "601988.XSHG", "000068.XSHE"]

   # 设置这个策略当中会用到的参数，在策略中可以随时调用，这个策略使用长短均线，我们在这里设定长线和短线的区间，在调试寻找最佳区间的时候只需要在这里进行数值改动
   #  context.cash_limit = 5000
    context.SHORTPERIOD = 20
    context.LONGPERIOD = 120


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑a

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！

    # 因为策略需要用到均线，所以需要读取历史数据
    for stock in context.stocks:
        prices = history(context.LONGPERIOD+1,'1d','close')[stock].values

        # 使用talib计算长短两根均线，均线以array的格式表达
        short_avg = talib.SMA(prices,context.SHORTPERIOD)
        long_avg = talib.SMA(prices,context.LONGPERIOD)

        plot("short avg",short_avg[-1])
        plot("long avg",long_avg[-1])

        # 计算现在portfolio中股票的仓位
        curPosition = context.portfolio.positions[stock].quantity
        # 计算现在portfolio中的现金可以购买多少股票
        shares = context.portfolio.cash/bar_dict[stock].close


        # 如果短均线从上往下跌破长均线，也就是在目前的bar短线平均值低于长线平均值，而上一个bar的短线平均值高于长线平均值
        if short_avg[-1]-long_avg[-1]<0 and short_avg[-2]-long_avg[-2]>0 and curPosition>0:
        #进行清仓
            order_target_value(stock,0)

        # 如果短均线从下往上突破长均线，为入场信号
        if short_avg[-1]-long_avg[-1]>0 and short_avg[-2]-long_avg[-2]<0:
        #满仓入股
            order_shares(stock,shares)
