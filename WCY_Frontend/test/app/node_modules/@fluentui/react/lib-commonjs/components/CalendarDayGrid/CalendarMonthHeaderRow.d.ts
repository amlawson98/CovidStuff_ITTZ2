import * as React from 'react';
import { ICalendarDayGridProps, ICalendarDayGridStyles } from './CalendarDayGrid.types';
import { IProcessedStyleSet } from '@fluentui/style-utilities';
import { IDayInfo } from './CalendarDayGrid.base';
export interface ICalendarDayMonthHeaderRowProps extends ICalendarDayGridProps {
    weeks: IDayInfo[][];
    classNames: IProcessedStyleSet<ICalendarDayGridStyles>;
}
export declare const CalendarMonthHeaderRow: React.FunctionComponent<ICalendarDayMonthHeaderRowProps>;
