import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    root: __dirname,
  },
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination:
          "https://ub4r9j3fl2.execute-api.eu-west-1.amazonaws.com/api/v1/:path*",
      },
    ];
  },
};

export default nextConfig;
