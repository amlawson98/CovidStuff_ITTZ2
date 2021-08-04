// This file mimics styles and mixins from _General.Mixins.scss
define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.noWrap = exports.normalize = void 0;
    exports.normalize = {
        boxShadow: 'none',
        margin: 0,
        padding: 0,
        boxSizing: 'border-box',
    };
    exports.noWrap = {
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
    };
});
//# sourceMappingURL=GeneralStyles.js.map