// frontend/next.config.mjs
/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
      NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL,
      AUTH0_SECRET: process.env.AUTH0_SECRET,
      AUTH0_BASE_URL: process.env.AUTH0_BASE_URL,
      AUTH0_ISSUER_BASE_URL: process.env.AUTH0_ISSUER_BASE_URL,
      AUTH0_CLIENT_ID: process.env.AUTH0_CLIENT_ID,
      AUTH0_CLIENT_SECRET: process.env.AUTH0_CLIENT_SECRET,
    },
  };
  
  export default nextConfig;
  