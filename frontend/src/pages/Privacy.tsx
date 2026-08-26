export default function Privacy() {
  return (
    <div className="min-h-screen bg-[#F7FAF7] py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="bg-white rounded-2xl shadow-sm p-8 md:p-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Privacy Policy</h1>
          <p className="text-sm text-gray-500 mb-8">Last Updated: August 2026 • Effective: Immediately</p>

          <div className="space-y-8 text-gray-700 text-sm leading-relaxed">
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">1. Overview</h2>
              <p>PlacementPro ("we", "us", "our") respects your privacy. This Privacy Policy explains how we collect, use, and protect your personal data when you use our Platform.</p>
              <p className="mt-2 text-amber-600 font-medium">⚠️ We are committed to protecting your data and complying with applicable privacy laws, including GDPR and the Indian IT Act.</p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">2. Information We Collect</h2>
              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold">2.1 Personal Information</h3>
                  <ul className="list-disc pl-6 mt-1 space-y-1">
                    <li><strong>Identity Data:</strong> Name, email address, phone number</li>
                    <li><strong>Profile Data:</strong> Username, profile picture, bio</li>
                    <li><strong>Academic Data:</strong> College, degree, year of graduation (optional)</li>
                    <li><strong>Employment Data:</strong> Current job, experience (optional)</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold">2.2 Usage Data</h3>
                  <ul className="list-disc pl-6 mt-1 space-y-1">
                    <li>Problems solved</li>
                    <li>Interviews taken</li>
                    <li>Progress and scores</li>
                    <li>Learning paths completed</li>
                    <li>Time spent on platform</li>
                    <li>Feature usage (resume builder, ATS, etc.)</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold">2.3 Device & Technical Data</h3>
                  <ul className="list-disc pl-6 mt-1 space-y-1">
                    <li>IP address</li>
                    <li>Browser type and version</li>
                    <li>Device type and OS</li>
                    <li>Cookies and tracking data</li>
                    <li>Log data (pages visited, clicks, errors)</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold">2.4 Payment Information</h3>
                  <ul className="list-disc pl-6 mt-1 space-y-1">
                    <li>Payment is processed through PayPal.</li>
                    <li><strong>We do not store credit card or banking information.</strong></li>
                    <li>We receive payment confirmation and transaction ID.</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">3. How We Use Your Data</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li><strong>To Provide Services:</strong> Grant access to courses, features, and personalized content.</li>
                <li><strong>To Improve Platform:</strong> Analyze usage, fix bugs, and enhance user experience.</li>
                <li><strong>To Communicate:</strong> Send invoices, updates, and important notifications.</li>
                <li><strong>To Personalize:</strong> Recommend content based on your progress and interests.</li>
                <li><strong>To Ensure Security:</strong> Detect and prevent fraud, abuse, and unauthorized access.</li>
                <li><strong>To Comply with Law:</strong> Fulfill legal obligations and respond to lawful requests.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">4. Legal Basis for Processing (GDPR)</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li><strong>Consent:</strong> You have given explicit consent for processing your data.</li>
                <li><strong>Contract:</strong> Processing is necessary for fulfilling our service agreement.</li>
                <li><strong>Legal Obligation:</strong> Compliance with applicable laws and regulations.</li>
                <li><strong>Legitimate Interest:</strong> Improving our services and ensuring security.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">5. Data Storage & Security</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>Data is stored securely on MongoDB Atlas (cloud) and local servers.</li>
                <li>All data is encrypted in transit (TLS 1.3) and at rest.</li>
                <li>Access is restricted to authorized personnel only.</li>
                <li>We implement industry-standard security measures.</li>
                <li>Data is retained for as long as your account is active.</li>
                <li>You may request deletion of your data at any time.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">6. Third-Party Services</h2>
              <div className="space-y-3">
                <p>We use the following third-party services that process your data:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li><strong>PayPal:</strong> Payment processing. <a href="https://www.paypal.com/us/legal" target="_blank" rel="noopener noreferrer" className="text-green-600 hover:underline">View their privacy policy</a>.</li>
                  <li><strong>OpenRouter:</strong> AI services. Anonymized data only (no personal data is shared).</li>
                  <li><strong>MongoDB Atlas:</strong> Cloud database provider. <a href="https://www.mongodb.com/legal/privacy" target="_blank" rel="noopener noreferrer" className="text-green-600 hover:underline">View their privacy policy</a>.</li>
                  <li><strong>Cloudflare:</strong> CDN and DDoS protection. <a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener noreferrer" className="text-green-600 hover:underline">View their privacy policy</a>.</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">7. Cookies</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>We use cookies to remember your login status, track progress, and analyze usage.</li>
                <li>You can disable cookies in your browser settings.</li>
                <li>We do not use tracking cookies for advertising purposes.</li>
                <li>Essential cookies cannot be disabled as they are required for functionality.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">8. Your Rights</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li><strong>Access:</strong> Request a copy of your data.</li>
                <li><strong>Rectification:</strong> Correct inaccurate or incomplete data.</li>
                <li><strong>Deletion:</strong> Request deletion of your data ("Right to be Forgotten").</li>
                <li><strong>Restriction:</strong> Restrict processing of your data.</li>
                <li><strong>Portability:</strong> Request your data in a machine-readable format.</li>
                <li><strong>Objection:</strong> Object to processing for marketing purposes.</li>
              </ul>
              <p className="mt-3">To exercise any of these rights, email us at <a href="mailto:privacy@placementpro.com" className="text-green-600 hover:underline">privacy@placementpro.com</a>.</p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">9. Data Breach Notification</h2>
              <p>In the event of a data breach, we will:</p>
              <ul className="list-disc pl-6 mt-2 space-y-1">
                <li>Notify affected users within 72 hours (GDPR requirement).</li>
                <li>Inform the relevant data protection authorities.</li>
                <li>Take immediate steps to mitigate the breach.</li>
                <li>Provide guidance to affected users.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">10. Children's Privacy</h2>
              <p>We do not knowingly collect data from children under 13. If you believe we have collected data from a child, contact us immediately and we will delete it.</p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">11. Changes to Privacy Policy</h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>We may update this Privacy Policy periodically.</li>
                <li>We will notify you via email or platform notification of significant changes.</li>
                <li>Continued use constitutes acceptance of the updated policy.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">12. Contact Information</h2>
              <p><strong>For privacy inquiries:</strong></p>
              <ul className="list-none space-y-1 mt-2">
                <li>📧 Email: <a href="mailto:privacy@placementpro.com" className="text-green-600 hover:underline">privacy@placementpro.com</a></li>
                <li>📧 General: <a href="mailto:support@placementpro.com" className="text-green-600 hover:underline">support@placementpro.com</a></li>
                <li>📍 Address: [Your Business Address]</li>
                <li>📞 Phone: [Your Phone Number]</li>
              </ul>
              <p className="mt-3 text-sm text-gray-500">For GDPR-related inquiries, our Data Protection Officer (DPO) can be reached at dpo@placementpro.com.</p>
            </section>

            <div className="border-t border-gray-200 pt-6 mt-8 text-xs text-gray-400">
              <p>By using PlacementPro, you agree to this Privacy Policy.</p>
              <p className="mt-1">Last Updated: August 2026 • Version: 2.0</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
