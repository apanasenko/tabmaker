import { isFunction, mapValues } from 'lodash';


export const mapProps = (props = {}) => (route: any) => {
  const { params } = route;
  return mapValues(
    props,
    (apply, name) => (isFunction(apply)
      ? params[name] && apply(params[name], route)
      : apply),
  );
};
