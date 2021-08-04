import * as React from 'react';
import { IImageProps, ImageLoadState } from './Image.types';
export interface IImageState {
    loadState?: ImageLoadState;
}
export declare const ImageBase: React.FunctionComponent<IImageProps>;
