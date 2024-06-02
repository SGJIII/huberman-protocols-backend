// frontend/src/utils/withAuth.js
import { withPageAuthRequired } from '@auth0/nextjs-auth0';

const withAuth = (Component) => {
  return withPageAuthRequired(Component);
};

export default withAuth;