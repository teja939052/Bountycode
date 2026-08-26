import { useState, useEffect } from "react";
import { motion } from "framer-motion";

export default function CookieBanner() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem("cookie_consent");
    if (!consent) {
      setVisible(true);
    }
  }, []);

  const accept = () => {
    localStorage.setItem("cookie_consent", "accepted");
    setVisible(false);
  };

  const reject = () => {
    localStorage.setItem("cookie_consent", "rejected");
    setVisible(false);
  };

  if (!visible) return null;

  return (
    <motion.div
      initial={{ y: 100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 shadow-lg p-4"
    >
      <div className="container mx-auto max-w-4xl flex flex-col sm:flex-row items-center justify-between gap-4">
        <p className="text-sm text-gray-600">
          We use cookies to improve your experience. By using our platform, you agree to our{" "}
          <a href="/privacy" className="text-green-600 hover:underline">Privacy Policy</a>{" "}
          and{" "}
          <a href="/terms" className="text-green-600 hover:underline">Terms & Conditions</a>.
        </p>
        <div className="flex gap-3">
          <button
            onClick={reject}
            className="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 transition-all"
          >
            Reject
          </button>
          <button
            onClick={accept}
            className="px-6 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition-all"
          >
            Accept All
          </button>
        </div>
      </div>
    </motion.div>
  );
}
