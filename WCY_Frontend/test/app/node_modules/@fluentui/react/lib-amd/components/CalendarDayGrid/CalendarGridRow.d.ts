import * as React from 'react';
import { ICalendarDayGridProps, ICalendarDayGridStyles } from './CalendarDayGrid.types';
import { IProcessedStyleSet } from '@fluentui/style-utilities';
import { IDayInfo, IWeekCorners } from './CalendarDayGrid.base';
export interface ICalendarGridRowProps extends ICalendarDayGridProps {
    classNames: IProcessedStyleSet<ICalendarDayGridStyles>;
    weeks: IDayInfo[][];
    week: IDayInfo[];
    weekIndex: number;
    weekCorners?: IWeekCorners;
    ariaHidden?: boolean;
    rowClassName?: string;
    ariaRole?: string;
    navigatedDayRef: React.RefObject<HTMLButtonElement>;
    activeDescendantId: string;
    calculateRoundedStyles(classNames: IProcessedStyleSet<ICalendarDayGridStyles>, above: boolean, below: boolean, left: boolean, right: boolean): string;
    getDayInfosInRangeOfDay(dayToCompare: IDayInfo): IDayInfo[];
    getRefsFromDayInfos(dayInfosInRange: IDayInfo[]): (HTMLElement | null)[];
}
export declare const CalendarGridRow: React.FunctionComponent<ICalendarGridRowProps>;
