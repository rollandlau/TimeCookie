# -*- coding=utf-8 -*-
# 文件名：TimeStamp.py
# 作  者：liuzhe
# 日  期：2013-9-21
# 修改人：无
# 描  述：时间的数据结构
import datetime
import sys
import time

class DateTimeEx(object):
    '''
    Convert Unix style time to Year,Month,Day,Hour,Minute,Second
    Constructor function input： Unix style timestamp
    Call GetTime() to get converted time:(2013,10,10,22,21,10)
    '''
    LeapYear_seconds = 31622400
    AverageYear_seconds = 31536000
    BigMonth_seconds = 2678400
    LiteMonth_seconds = 2592000
    FebLeapMonth_seconds = 2505600
    FebLiteMonth_seconds = 2419200
    
    AverageMonth_seconds = 2635200
    day_seconds = 86400
    BigMonth = (1,3,5,7,8,10,12)
    year = 0
    month = 0
    day = 0
    hour = 0
    minute = 0
    second = 0
    
    def IsLeapYear(self, Year):
        if (Year % 400 == 0) or ((Year % 4 == 0 ) and (Year % 100 != 0)):
            return True
        else:
            return False
            
    def __init__(self, ticktack, timeoffset = 8):
        #icktack: the seconds passed after 1970-1-1-0-0-0
        try:
            #calculate year count
            #YearTick begin from 0(1970)
            YearTick = 0
            
            if ticktack > 0:
                CurrentYear = 1970
                while (True):
                    #Add seconds to YearTick until it greater than ticktack(which means reach the year we want)
                    if self.IsLeapYear(CurrentYear):
                        if (YearTick + self.LeapYear_seconds) <= ticktack:
                            YearTick += self.LeapYear_seconds
                        else:
                            break
                    else:
                        if (YearTick + self.AverageYear_seconds) <= ticktack:
                            YearTick += self.AverageYear_seconds
                        else:
                            break
                    CurrentYear += 1
                #minus these seconds counted as year
                ticktack = ticktack - YearTick
                self.year = CurrentYear
                
                CurrentMonth = 1
                MonthTick = 0
                while (True):
                    #Just like processing year
                    if (CurrentMonth in self.BigMonth):
                        if (MonthTick + self.BigMonth_seconds) <= ticktack:
                            MonthTick += self.BigMonth_seconds
                        else:
                            break
                    elif CurrentMonth == 2:
                        if self.IsLeapYear(self.year):
                            if (MonthTick + self.FebLeapMonth_seconds) <= ticktack:
                                MonthTick += self.FebLeapMonth_seconds
                            else:
                                break
                        else:
                            if (MonthTick + self.FebLiteMonth_seconds) <= ticktack:
                                MonthTick += self.FebLiteMonth_seconds
                            else:
                                break
                    else:
                        if (MonthTick + self.LiteMonth_seconds) <= ticktack:
                            MonthTick += self.LiteMonth_seconds
                        else:
                            break
                    
                    CurrentMonth += 1
                    
                self.month = CurrentMonth
                ticktack = ticktack - MonthTick
                
                self.day = ticktack / self.day_seconds
                ticktack = ticktack % self.day_seconds
                
                self.hour = ticktack / 3600
                ticktack = ticktack % 3600
                
                self.minute = ticktack / 60
                ticktack = ticktack % 60
                
                self.second = ticktack
                
            else:
                #Negative ticktack means the time before 1970-1-1
                
                CurrentYear = 1970
                while (True):
                    CurrentYear -= 1
                    #If ticktack + seconds of a year is greater than 0,means we got the year offset we want
                    if self.IsLeapYear(CurrentYear):
                        if (ticktack + self.LeapYear_seconds) <= 0:
                            ticktack += self.LeapYear_seconds
                        else:
                            break
                    else:
                        if (ticktack + self.AverageYear_seconds) <= 0:
                            ticktack += self.AverageYear_seconds
                        else:
                            break
                        
                self.year = CurrentYear
                
                CurrentMonth = 12
                while (True):
                    if (CurrentMonth in self.BigMonth):
                        if (ticktack + self.BigMonth_seconds) <= 0:
                            ticktack += self.BigMonth_seconds
                        else:
                            break
                    elif CurrentMonth == 2:
                        if self.IsLeapYear(self.year):
                            if (ticktack + self.FebLeapMonth_seconds) <= 0:
                                ticktack += self.FebLeapMonth_seconds
                            else:
                                break
                        else:
                            if (ticktack + self.FebLiteMonth_seconds) <= 0:
                                ticktack += self.FebLiteMonth_seconds
                            else:
                                break
                    else:
                        if (ticktack + self.LiteMonth_seconds) <= 0:
                            ticktack += self.LiteMonth_seconds
                        else:
                            break
                    
                    CurrentMonth -= 1
                    
                self.month = CurrentMonth
                
                TmpDay = abs(ticktack) / self.day_seconds
                ticktack = ticktack + TmpDay * self.day_seconds
                
                if CurrentMonth in self.BigMonth:
                    TmpDay = 31 - TmpDay
                elif CurrentMonth == 2:
                    if self.IsLeapYear(self.year):
                        TmpDay = 29 - TmpDay
                    else:
                        TmpDay = 28 - TmpDay
                else:
                    TmpDay = 30 -TmpDay
                
                self.day = TmpDay
                
                HourOffset = abs(ticktack) / 3600 
                self.hour = 23 - HourOffset 
                ticktack = ticktack + HourOffset * 3600
                
                MinuteOffset = abs(ticktack) / 60
                self.minute = 59 - MinuteOffset
                ticktack = ticktack + MinuteOffset * 60
                
                self.second = 59 - abs(ticktack)
        except:
            sys.stdout.write('%s\n'%(str(sys.exc_info())))
    
    def GetTime(self):
        return (self.year, self.month, self.day, self.hour, self.minute, self.second)

if __name__ == '__main__':
    i= 0
    while True:
        myobj = DateTimeEx(-638273934)
        print myobj.GetTime()
        time.sleep(0.1)