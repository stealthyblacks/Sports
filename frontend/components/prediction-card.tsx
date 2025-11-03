"use client"

import { motion } from "framer-motion"
import Link from "next/link"

interface PredictionCardProps {
  id: string
  homeTeam: string
  awayTeam: string
  prediction: string
  odds: string
  date: string
}

export function PredictionCard({ id, homeTeam, awayTeam, prediction, odds, date }: PredictionCardProps) {
  return (
    <Link href={`/predictions/${id}`}>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        whileInView={{ opacity: 1, y: 0 }}
        whileHover={{ y: -4, boxShadow: "0 10px 25px rgba(22, 163, 74, 0.15)" }}
        whileTap={{ scale: 0.98 }}
        transition={{ duration: 0.3 }}
        className="bg-card border border-border rounded-lg p-4 cursor-pointer hover:shadow-lg transition-shadow"
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex-1">
            <p className="text-sm text-muted-foreground">{date}</p>
            <div className="flex items-center gap-2 mt-1">
              <span className="font-semibold text-sm">{homeTeam}</span>
              <span className="text-xs text-muted-foreground">vs</span>
              <span className="font-semibold text-sm">{awayTeam}</span>
            </div>
          </div>
        </div>
        <motion.div whileHover={{ scale: 1.05 }} className="bg-primary/10 rounded px-3 py-2 mb-2">
          <p className="text-sm font-medium text-primary">{prediction}</p>
        </motion.div>
        <p className="text-xs text-muted-foreground">Odds: {odds}</p>
      </motion.div>
    </Link>
  )
}
