import * as React from 'react';
import { IContextualMenuProps, IContextualMenuItem } from './ContextualMenu.types';
import { DirectionalHint } from '../../common/DirectionalHint';
export interface IContextualMenuState {
    contextualMenuItems?: IContextualMenuItem[];
    contextualMenuTarget?: Element;
    positions?: any;
    slideDirectionalClassName?: string;
    subMenuId?: string;
    submenuDirection?: DirectionalHint;
}
export declare function getSubmenuItems(item: IContextualMenuItem): IContextualMenuItem[] | undefined;
/**
 * Returns true if a list of menu items can contain a checkbox
 */
export declare function canAnyMenuItemsCheck(items: IContextualMenuItem[]): boolean;
export declare const ContextualMenuBase: React.FunctionComponent<IContextualMenuProps>;
