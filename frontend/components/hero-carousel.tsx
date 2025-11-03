"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"

const players = [
  {
    id: 1,
    name: "Cristiano Ronaldo",
    quote: "Your dedication will define your destiny.",
    image: "/cristiano-ronaldo-football-player.jpg",
  },
  {
    id: 2,
    name: "Lionel Messi",
    quote: "When you stop dreaming, you stop living.",
    image: "/lionel-messi-football-player.jpg",
  },
  {
    id: 3,
    name: "Neymar Jr",
    quote: "Football is passion and joy.",
    image: "/neymar-jr-football-player.jpg",
  },
]

export function HeroCarousel() {
  const [current, setCurrent] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % players.length)
    }, 5000)
    return () => clearInterval(timer)
  }, [])

  return (
    <div className="relative h-[500px] w-full overflow-hidden rounded-2xl shadow-lg">
      {players.map((player, index) => (
        <motion.div
          key={player.id}
          initial={{ opacity: 0 }}
          animate={{ opacity: index === current ? 1 : 0 }}
          transition={{ duration: 1 }}
          className="absolute inset-0"
        >
          <motion.img
            initial={{ scale: 1.1 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.8 }}
            src={player.image || "/placeholder.svg"}
            alt={player.name}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={index === current ? { y: 0, opacity: 1 } : { y: 20, opacity: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="absolute bottom-0 left-0 right-0 p-8 text-white"
          >
            <h2 className="text-4xl font-bold mb-2">{player.name}</h2>
            <p className="text-lg italic">"{player.quote}"</p>
          </motion.div>
        </motion.div>
      ))}

      {/* Carousel controls */}
      <motion.div className="absolute bottom-4 right-4 flex gap-2 z-10">
        {players.map((_, index) => (
          <motion.button
            whileHover={{ scale: 1.2 }}
            whileTap={{ scale: 0.95 }}
            key={index}
            onClick={() => setCurrent(index)}
            className={`w-2 h-2 rounded-full transition-all ${index === current ? "bg-white w-8" : "bg-white/50"}`}
          />
        ))}
      </motion.div>
    </div>
  )
}
