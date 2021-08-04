import * as React from 'react';
import { IDayInfo } from './CalendarDayGrid.base';
import { ICalendarGridRowProps } from './CalendarGridRow';
export interface ICalendarGridDayCellProps extends ICalendarGridRowProps {
    day: IDayInfo;
    dayIndex: number;
}
export declare const CalendarGridDayCell: React.FunctionComponent<ICalendarGridDayCellProps>;
