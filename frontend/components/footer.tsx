"use client"

import { motion } from "framer-motion"

export function Footer() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: {
      opacity: 1,
      y: 0,
    },
  }

  return (
    <footer className="bg-slate-900 text-white border-t border-border mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          className="grid grid-cols-1 md:grid-cols-4 gap-8"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <motion.div variants={itemVariants}>
            <h3 className="font-bold text-lg mb-4">FootballPro</h3>
            <p className="text-gray-400 text-sm">Expert football predictions and insights.</p>
          </motion.div>
          <motion.div variants={itemVariants}>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <motion.a href="/" whileHover={{ x: 4 }} className="hover:text-white transition inline-block">
                  Home
                </motion.a>
              </li>
              <li>
                <motion.a
                  href="/predictions"
                  whileHover={{ x: 4 }}
                  className="hover:text-white transition inline-block"
                >
                  Predictions
                </motion.a>
              </li>
              <li>
                <motion.a href="/news" whileHover={{ x: 4 }} className="hover:text-white transition inline-block">
                  News
                </motion.a>
              </li>
            </ul>
          </motion.div>
          <motion.div variants={itemVariants}>
            <h4 className="font-semibold mb-4">Follow Us</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <motion.a href="#" whileHover={{ x: 4 }} className="hover:text-white transition inline-block">
                  Twitter
                </motion.a>
              </li>
              <li>
                <motion.a href="#" whileHover={{ x: 4 }} className="hover:text-white transition inline-block">
                  Facebook
                </motion.a>
              </li>
              <li>
                <motion.a href="#" whileHover={{ x: 4 }} className="hover:text-white transition inline-block">
                  Instagram
                </motion.a>
              </li>
            </ul>
          </motion.div>
          <motion.div variants={itemVariants}>
            <h4 className="font-semibold mb-4">Legal</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <motion.a href="#" whileHover={{ x: 4 }} className="hover:text-white transition inline-block">
                  Privacy
                </motion.a>
              </li>
              <li>
                <motion.a href="#" whileHover={{ x: 4 }} className="hover:text-white transition inline-block">
                  Terms
                </motion.a>
              </li>
              <li>
                <motion.a href="#" whileHover={{ x: 4 }} className="hover:text-white transition inline-block">
                  Contact
                </motion.a>
              </li>
            </ul>
          </motion.div>
        </motion.div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400 text-sm">
          <p>&copy; 2025 FootballPro. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
