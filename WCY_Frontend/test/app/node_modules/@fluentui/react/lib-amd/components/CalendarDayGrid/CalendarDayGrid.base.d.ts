import * as React from 'react';
import { IDay } from '@fluentui/date-time-utilities';
import { ICalendarDayGridProps } from './CalendarDayGrid.types';
export interface IWeekCorners {
    [key: string]: string;
}
export interface IDayInfo extends IDay {
    onSelected: () => void;
    setRef(element: HTMLElement | null): void;
}
export declare const CalendarDayGridBase: React.FunctionComponent<ICalendarDayGridProps>;
