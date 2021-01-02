import React, { lazy, Suspense } from 'react';

const LazyInput = lazy(() => import('./Input'));

const Input = props => (
  <Suspense fallback={null}>
    <LazyInput {...props} />
  </Suspense>
);

export default Input;
