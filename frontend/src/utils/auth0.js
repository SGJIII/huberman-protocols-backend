import { initAuth0 } from '@auth0/nextjs-auth0';

export default initAuth0({
  domain: process.env.AUTH0_ISSUER_BASE_URL,
  clientId: process.env.AUTH0_CLIENT_ID,
  clientSecret: process.env.AUTH0_CLIENT_SECRET,
  scope: 'openid profile email',
  redirectUri: process.env.AUTH0_BASE_URL + '/api/auth/callback',
  postLogoutRedirectUri: process.env.AUTH0_BASE_URL,
  session: {
    cookieSecret: process.env.AUTH0_SECRET,
  },
});
