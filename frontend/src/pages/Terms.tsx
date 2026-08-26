export default function Terms() {
  return (
    <div className="min-h-screen bg-[#F7FAF7] py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="bg-white rounded-2xl shadow-sm p-8 md:p-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Terms & Conditions</h1>
          <p className="text-sm text-gray-500 mb-8">Last Updated: August 2026 • Effective: Immediately</p>

          <div className="space-y-8 text-gray-700 text-sm leading-relaxed">
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">1. Acceptance of Terms</h2>
              <p>By accessing or using PlacementPro ("the Platform"), you agree to be bound by these Terms & Conditions ("Terms"). If you do not agree to these Terms, you must not use the Platform.</p>
              <p className="mt-2">These Terms constitute a legally binding agreement between you ("User") and PlacementPro ("Company", "We", "Us").</p>
              <p className="mt-2 text-amber-600 font-medium">⚠️ By using the Platform, you acknowledge that you have read, understood, and accepted these Terms.</p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">2. Eligibility</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>You must be at least <strong>13 years old</strong> to use the Platform.</li>
                <li>If you are under 18, you confirm that you have parental/guardian consent.</li>
                <li>You must not be barred from using the Platform under applicable law.</li>
                <li>You must provide accurate, complete, and up-to-date information.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">3. Account & Security</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>You are solely responsible for maintaining the confidentiality of your account credentials.</li>
                <li>You are responsible for all activities that occur under your account.</li>
                <li>You must immediately notify us of any unauthorized use of your account.</li>
                <li>We reserve the right to suspend or terminate accounts that violate these Terms.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">4. Subscription & Payment</h2>
              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold">4.1 Pricing & Plans</h3>
                  <ul className="list-disc pl-6 mt-1 space-y-1">
                    <li><strong>Free Tier:</strong> $0/month — Limited features as displayed on the Platform.</li>
                    <li><strong>Pro:</strong> $9/month — Unlimited access to all features.</li>
                    <li><strong>Lifetime:</strong> $39 — One-time payment for permanent access.</li>
                  </ul>
                  <p className="text-xs text-gray-500 mt-1">Prices are subject to change. We will notify you 30 days before any price change.</p>
                </div>
                <div>
                  <h3 className="font-semibold">4.2 Billing</h3>
                  <ul className="list-disc pl-6 mt-1 space-y-1">
                    <li>Payments are processed securely through PayPal.</li>
                    <li>You authorize us to charge your selected payment method.</li>
                    <li>Subscription fees are billed in advance on a recurring basis.</li>
                    <li>If payment fails, we may suspend your access until payment is resolved.</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold">4.3 Cancellation</h3>
                  <ul className="list-disc pl-6 mt-1 space-y-1">
                    <li>You can cancel your subscription at any time from your account settings.</li>
                    <li>Cancellation takes effect at the end of the current billing cycle.</li>
                    <li>No refunds are provided for partial billing periods.</li>
                    <li>After cancellation, you will lose access to Pro features.</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">5. Refund Policy</h2>
              <div className="space-y-3">
                <p><strong>5.1 7-Day Money-Back Guarantee</strong></p>
                <p>We offer a 7-day money-back guarantee for all paid subscriptions. If you are not satisfied, you may request a full refund within 7 days of purchase.</p>

                <p className="mt-3"><strong>5.2 How to Request</strong></p>
                <p>Email us at <a href="mailto:support@placementpro.com" className="text-green-600 hover:underline">support@placementpro.com</a> with:</p>
                <ul className="list-disc pl-6 mt-1 space-y-1">
                  <li>Your registered email address</li>
                  <li>PayPal Transaction ID</li>
                  <li>Brief reason for refund</li>
                </ul>

                <p className="mt-3"><strong>5.3 Processing</strong></p>
                <ul className="list-disc pl-6 mt-1 space-y-1">
                  <li>Refunds are processed within 5-7 business days.</li>
                  <li>The amount will be credited to your original payment method.</li>
                  <li>After 7 days, no refunds will be issued.</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">6. User Obligations</h2>
              <p className="font-semibold text-red-600">You agree NOT to:</p>
              <ul className="list-disc pl-6 mt-2 space-y-2">
                <li>Share your account credentials with others.</li>
                <li>Use the Platform for any illegal or unauthorized purpose.</li>
                <li>Cheat, hack, or exploit the Platform in any way.</li>
                <li>Submit false or misleading information.</li>
                <li>Impersonate another person or entity.</li>
                <li>Upload malicious code, viruses, or harmful content.</li>
                <li>Scrape, crawl, or extract data from the Platform.</li>
                <li>Interfere with or disrupt the Platform's functionality.</li>
                <li>Use the Platform to harass, abuse, or harm others.</li>
              </ul>
              <p className="mt-3 text-amber-600 font-medium">⚠️ Violation of these obligations may result in immediate termination of your account without refund.</p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">7. Intellectual Property</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>All content on the Platform (courses, questions, designs, code, text, graphics, logos) is owned by PlacementPro.</li>
                <li>You may not reproduce, distribute, or create derivative works without explicit written permission.</li>
                <li>Your submitted content (solutions, code, etc.) becomes our property upon submission.</li>
                <li>We do not claim ownership of your personal data (as per Privacy Policy).</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">8. Data & Privacy</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>We collect and process data as described in our <a href="/privacy" className="text-green-600 hover:underline">Privacy Policy</a>.</li>
                <li>We use your data to provide, improve, and personalize the Platform.</li>
                <li>We do not sell your personal data to third parties.</li>
                <li>You have the right to access, correct, or delete your data at any time.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">9. Limitation of Liability</h2>
              <div className="space-y-3">
                <p><strong>TO THE MAXIMUM EXTENT PERMITTED BY LAW:</strong></p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>The Platform is provided "AS IS" and "AS AVAILABLE" without warranties of any kind.</li>
                  <li>We do not guarantee that the Platform will be error-free or uninterrupted.</li>
                  <li>We are not liable for any indirect, incidental, special, consequential, or punitive damages.</li>
                  <li>We are not responsible for third-party services (e.g., PayPal, OpenRouter, MongoDB).</li>
                  <li>We are not liable for any loss of data, revenue, or opportunities.</li>
                  <li>Our total liability shall not exceed the amount you paid us in the past 12 months.</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">10. Dispute Resolution</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>These Terms are governed by the laws of India.</li>
                <li>Any disputes shall be resolved through <strong>mandatory arbitration</strong> in [Your City, India].</li>
                <li>You waive the right to participate in class action lawsuits.</li>
                <li>Small claims court is available for disputes under ₹50,000.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">11. Termination</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>We may suspend or terminate your account at any time without notice if you violate these Terms.</li>
                <li>You may delete your account at any time from account settings.</li>
                <li>Upon termination, you lose access to all Pro features and your data may be deleted.</li>
                <li>No refunds are provided for terminated accounts due to violations.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">12. Changes</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>We may update these Terms from time to time.</li>
                <li>We will notify you via email or platform notification of significant changes.</li>
                <li>Continued use of the Platform constitutes acceptance of the updated Terms.</li>
                <li>If you disagree with the changes, you must stop using the Platform.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">13. Contact Information</h2>
              <p><strong>For legal inquiries:</strong></p>
              <ul className="list-none space-y-1 mt-2">
                <li>📧 Email: <a href="mailto:legal@placementpro.com" className="text-green-600 hover:underline">legal@placementpro.com</a></li>
                <li>📞 Phone: [Your Phone Number]</li>
                <li>📍 Address: [Your Business Address]</li>
              </ul>
            </section>

            <div className="border-t border-gray-200 pt-6 mt-8 text-xs text-gray-400">
              <p>By using PlacementPro, you agree to these Terms & Conditions.</p>
              <p className="mt-1">Last Updated: August 2026 • Version: 2.0</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
