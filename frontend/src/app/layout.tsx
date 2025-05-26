import type { Metadata } from "next";
import { Inter } from "next/font/google";

import Provider from "@/redux/provider";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CapsLock",
  description: "PoC assessment",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Provider>
          <nav className="bg-white shadow">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex">
                  <div className="flex-shrink-0 flex items-center">
                    <span className="text-xl font-bold text-gray-900">CapsLock</span>
                  </div>
                </div>
              </div>
            </div>
          </nav>
          <main>{children}</main>
        </Provider>
      </body>
    </html>
  );
}
