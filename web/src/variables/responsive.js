// 반응형 웹 개발에 필요한 툴
const Responsive = {
    TABLET: 1200,
    MOBILE: 760
}
export const ResponsiveQuery = {
    MOBILE: {maxWidth: Responsive.MOBILE},
    TABLET: {minWidth: Responsive.MOBILE, maxWidth: Responsive.TABLET},
    PC:     {minWidth: Responsive.TABLET}
};