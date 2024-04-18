import { Roboto } from "next/font/google";
import "./globals.css";
import Navbar from "@/app/components/Navbar/Navbar";
import Footer from "@/app/components/Footer/Footer";

const roboto = Roboto({
  subsets: ["latin"],
  weight: ['400', '700'],
  display: "swap",
});

export const metadata = {
  title: "UP2040452 Cyber Security Chatbot",
  description: "A retrieval-augmented generation chatbot for Cyber Security. Part of UP2040452's Final Year Project.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={roboto.className}>
        <header>
          <Navbar />
        </header>
        <main>
          {children}
        </main>
        <footer>
          <Footer />
        </footer>
      </body>
    </html>
  );
}
