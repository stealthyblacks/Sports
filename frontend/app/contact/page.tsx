"use client"

import type React from "react"

import { useState } from "react"
import { motion } from "framer-motion"
import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { AdContainer } from "@/components/ad-container"

interface FAQItem {
  id: number
  question: string
  answer: string
}

const faqItems: FAQItem[] = [
  {
    id: 1,
    question: "How accurate are your predictions?",
    answer:
      "Our predictions are based on comprehensive statistical analysis, team form, head-to-head records, and expert insights. While we strive for accuracy, football is unpredictable and no prediction is guaranteed. We recommend reviewing our confidence levels and expert analysis before making betting decisions.",
  },
  {
    id: 2,
    question: "Can I use your predictions for legal betting?",
    answer:
      "Yes, you can use our predictions for legal sports betting. However, always ensure you are betting responsibly and within the laws of your jurisdiction. Please note that betting involves risk and you should only bet money you can afford to lose.",
  },
  {
    id: 3,
    question: "How often are predictions updated?",
    answer:
      "We update our predictions regularly as match dates approach. New predictions are typically published several days before matches to allow you time to analyze and make informed decisions. Real-time updates are provided for late-breaking team news or injuries.",
  },
  {
    id: 4,
    question: "Do you cover all football leagues?",
    answer:
      "We primarily focus on major football leagues including the Premier League, La Liga, Serie A, Bundesliga, and other top-tier European competitions. We also cover international matches and cup competitions. Coverage may vary by season.",
  },
  {
    id: 5,
    question: "Is there a subscription fee?",
    answer:
      "Basic predictions and analysis are free to all users. We may offer premium features with enhanced analysis, expert tips, and exclusive content for a subscription fee. Check our website for current pricing and subscription options.",
  },
  {
    id: 6,
    question: "How can I contact customer support?",
    answer:
      "You can reach our support team through this contact form, email, or live chat. We typically respond to inquiries within 24 hours. For urgent issues, please use our live chat feature.",
  },
]

export default function ContactPage() {
  const [expandedFAQ, setExpandedFAQ] = useState<number | null>(null)
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  })
  const [submitted, setSubmitted] = useState(false)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitted(true)
    setFormData({ name: "", email: "", subject: "", message: "" })
    setTimeout(() => setSubmitted(false), 5000)
  }

  return (
    <>
      <Navigation />
      <main className="bg-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Header */}
          <section className="mb-12 text-center">
            <h1 className="text-4xl lg:text-5xl font-bold text-foreground mb-4">Get in Touch</h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Have questions about our predictions? Need support? We'd love to hear from you.
            </p>
          </section>

          {/* Ad Banner */}
          <section className="mb-12">
            <AdContainer size="horizontal" />
          </section>

          {/* Contact Section */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
            {/* Contact Form */}
            <motion.div initial={{ opacity: 0, x: -20 }} whileInView={{ opacity: 1, x: 0 }} className="lg:col-span-2">
              <div className="bg-card border border-border rounded-lg p-8">
                <h2 className="text-2xl font-bold text-foreground mb-6">Send us a Message</h2>

                {submitted && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-6 p-4 bg-green-500/10 border border-green-500/20 rounded-lg text-green-600"
                  >
                    Thank you for your message! We'll get back to you soon.
                  </motion.div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-foreground mb-2">Full Name</label>
                      <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-3 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                        placeholder="John Doe"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-foreground mb-2">Email Address</label>
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-3 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                        placeholder="john@example.com"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-foreground mb-2">Subject</label>
                    <select
                      name="subject"
                      value={formData.subject}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 rounded-lg bg-background border border-border text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    >
                      <option value="">Select a subject</option>
                      <option value="prediction">Prediction Question</option>
                      <option value="feedback">General Feedback</option>
                      <option value="support">Technical Support</option>
                      <option value="partnership">Partnership Inquiry</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-foreground mb-2">Message</label>
                    <textarea
                      name="message"
                      value={formData.message}
                      onChange={handleInputChange}
                      required
                      rows={6}
                      className="w-full px-4 py-3 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary resize-none"
                      placeholder="Tell us what's on your mind..."
                    />
                  </div>

                  <button
                    type="submit"
                    className="w-full bg-primary text-primary-foreground py-3 rounded-lg font-medium hover:bg-primary/90 transition"
                  >
                    Send Message
                  </button>
                </form>
              </div>
            </motion.div>

            {/* Contact Info */}
            <motion.div initial={{ opacity: 0, x: 20 }} whileInView={{ opacity: 1, x: 0 }} className="space-y-6">
              <div className="bg-card border border-border rounded-lg p-6">
                <h3 className="font-bold text-foreground mb-4 flex items-center gap-2">
                  <span className="text-2xl">📧</span> Email
                </h3>
                <p className="text-muted-foreground text-sm">
                  <a href="mailto:support@footballpro.com" className="text-primary hover:underline">
                    support@footballpro.com
                  </a>
                </p>
              </div>

              <div className="bg-card border border-border rounded-lg p-6">
                <h3 className="font-bold text-foreground mb-4 flex items-center gap-2">
                  <span className="text-2xl">💬</span> Live Chat
                </h3>
                <p className="text-muted-foreground text-sm mb-4">Available Monday - Friday, 9am - 5pm UTC</p>
                <button className="w-full bg-primary text-primary-foreground py-2 rounded-lg font-medium hover:bg-primary/90 transition text-sm">
                  Start Chat
                </button>
              </div>

              <div className="bg-card border border-border rounded-lg p-6">
                <h3 className="font-bold text-foreground mb-4 flex items-center gap-2">
                  <span className="text-2xl">📱</span> Follow Us
                </h3>
                <div className="flex gap-4">
                  <a href="#" className="text-primary hover:text-primary/80 transition text-sm font-medium">
                    Twitter
                  </a>
                  <a href="#" className="text-primary hover:text-primary/80 transition text-sm font-medium">
                    Facebook
                  </a>
                  <a href="#" className="text-primary hover:text-primary/80 transition text-sm font-medium">
                    Instagram
                  </a>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Ad Banner */}
          <section className="mb-12">
            <AdContainer size="horizontal" />
          </section>

          {/* FAQ Section */}
          <section className="mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-8 text-center">Frequently Asked Questions</h2>
            <div className="max-w-3xl mx-auto space-y-4">
              {faqItems.map((item) => (
                <motion.div key={item.id} layout className="bg-card border border-border rounded-lg overflow-hidden">
                  <button
                    onClick={() => setExpandedFAQ(expandedFAQ === item.id ? null : item.id)}
                    className="w-full px-6 py-4 flex items-center justify-between hover:bg-muted transition text-left"
                  >
                    <span className="font-semibold text-foreground">{item.question}</span>
                    <motion.span
                      initial={{ rotate: 0 }}
                      animate={{ rotate: expandedFAQ === item.id ? 180 : 0 }}
                      className="text-primary text-xl"
                    >
                      ▼
                    </motion.span>
                  </button>
                  {expandedFAQ === item.id && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="px-6 py-4 border-t border-border bg-muted/30 text-muted-foreground"
                    >
                      {item.answer}
                    </motion.div>
                  )}
                </motion.div>
              ))}
            </div>
          </section>

          {/* Ad Banner */}
          <section className="mb-8">
            <AdContainer size="horizontal" />
          </section>
        </div>
      </main>
      <Footer />
    </>
  )
}
