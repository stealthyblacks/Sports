"use client"

import Link from "next/link"
import { motion } from "framer-motion"

interface NewsCardProps {
  id: string
  title: string
  summary: string
  thumbnail: string
  date: string
}

export function NewsCard({ id, title, summary, thumbnail, date }: NewsCardProps) {
  return (
    <Link href={`/news/${id}`}>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        whileInView={{ opacity: 1, y: 0 }}
        whileHover={{ y: -8, boxShadow: "0 12px 30px rgba(0, 0, 0, 0.15)" }}
        whileTap={{ scale: 0.98 }}
        className="bg-card border border-border rounded-lg overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
      >
        <motion.img
          whileHover={{ scale: 1.05 }}
          src={thumbnail || "/placeholder.svg"}
          alt={title}
          className="w-full h-40 object-cover"
        />
        <div className="p-4">
          <p className="text-xs text-muted-foreground mb-2">{date}</p>
          <h3 className="font-semibold text-sm mb-2 line-clamp-2">{title}</h3>
          <p className="text-xs text-muted-foreground line-clamp-2 mb-3">{summary}</p>
          <motion.div whileHover={{ x: 4 }}>
            <span className="text-primary text-sm font-medium hover:underline">Read More →</span>
          </motion.div>
        </div>
      </motion.div>
    </Link>
  )
}
