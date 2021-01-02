import React, { lazy, Suspense } from 'react';

const LazyOutput = lazy(() => import('./Output'));

const Output = props => (
  <Suspense fallback={null}>
    <LazyOutput {...props} />
  </Suspense>
);

export default Output;
