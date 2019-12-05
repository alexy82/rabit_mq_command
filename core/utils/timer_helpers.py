import time

import schedule


class Timer:
    @staticmethod
    def decorator(interval):
        def interval_decorator(func):
            def func_wrapper(self, **kwargs):
                schedule.every(interval).seconds.do(func,self,**kwargs)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            return func_wrapper
        return interval_decorator
