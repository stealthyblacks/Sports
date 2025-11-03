"use client"

import { motion } from "framer-motion"

export function AdContainer({ size = "vertical" }: { size?: "vertical" | "horizontal" }) {
  if (size === "horizontal") {
    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
        className="bg-gradient-to-r from-slate-100 to-slate-50 border border-border rounded-lg p-6 text-center"
      >
        <p className="text-xs text-muted-foreground mb-2">ADVERTISEMENT</p>
        <div className="bg-slate-200 h-24 rounded flex items-center justify-center text-muted-foreground text-sm">
          Ad Space - 728x90
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className="bg-gradient-to-b from-slate-100 to-slate-50 border border-border rounded-lg p-4 text-center"
    >
      <p className="text-xs text-muted-foreground mb-2">ADVERTISEMENT</p>
      <div className="bg-slate-200 h-40 rounded flex items-center justify-center text-muted-foreground text-xs">
        Ad Space - 300x250
      </div>
    </motion.div>
  )
}
