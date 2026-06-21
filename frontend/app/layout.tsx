import type { Metadata } from "next";
import { Bricolage_Grotesque } from "next/font/google";
import { GeistMono } from "geist/font/mono";
import { GeistSans } from "geist/font/sans";

import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { Footer } from "@/components/layout/Footer";
import { Navbar } from "@/components/layout/Navbar";
import { ThemeProvider } from "@/components/theme/ThemeProvider";
import {
  PaletteProvider,
  PALETTE_NO_FLASH_SCRIPT,
} from "@/components/theme/PaletteProvider";
import "./globals.css";

const bricolage = Bricolage_Grotesque({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-bricolage",
});

export const metadata: Metadata = {
  title: "NeuroScan — Brain Tumor MRI Analyzer",
  description:
    "An explainable brain-tumor MRI classifier with GradCAM heatmaps and local clinical reports. Educational & research use only.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${GeistSans.variable} ${GeistMono.variable} ${bricolage.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col">
        <script dangerouslySetInnerHTML={{ __html: PALETTE_NO_FLASH_SCRIPT }} />
        <div className="app-atmosphere" aria-hidden />
        <ThemeProvider>
          <PaletteProvider>
            <Navbar />
            <DisclaimerBanner variant="strip" />
            <main className="flex-1">{children}</main>
            <Footer />
          </PaletteProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
