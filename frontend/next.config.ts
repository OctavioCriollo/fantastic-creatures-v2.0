import type { NextConfig } from "next";
const NEXT_PUBLIC_BACKEND_API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL
const backendUrl = NEXT_PUBLIC_BACKEND_API_URL ? new URL(NEXT_PUBLIC_BACKEND_API_URL) : null;

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',       //API Port (Flask Server)
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: backendUrl?.hostname || '',
        // Si no hay puerto, no lo incluyas en el patrón
        ...(backendUrl?.port ? { port: backendUrl.port } : {}),
        pathname: '/**',
      }
    ],
  },
};

export default nextConfig;




