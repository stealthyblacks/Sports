"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { AdContainer } from "@/components/ad-container"
import predictions from "@/data/predictions.json"

export default function PredictionDetailsPage({ params }: { params: { id: string } }) {
  const prediction = predictions.find((p) => p.id === params.id)
  const [expandedMatch, setExpandedMatch] = useState<number | null>(null)

  if (!prediction) {
    return (
      <>
        <Navigation />
        <main className="bg-background min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-foreground mb-4">Prediction not found</h1>
            <a href="/predictions" className="text-primary font-medium hover:underline">
              ← Back to All Predictions
            </a>
          </div>
        </main>
        <Footer />
      </>
    )
  }

  return (
    <>
      <Navigation />
      <main className="bg-background">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Back Button */}
          <a
            href="/predictions"
            className="inline-flex items-center text-primary font-medium hover:text-primary/80 transition mb-8"
          >
            ← Back to All Predictions
          </a>

          {/* Main Prediction Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-card border border-border rounded-lg p-8 mb-8"
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Left: Match Info */}
              <div>
                <p className="text-sm text-muted-foreground mb-4">{prediction.date}</p>
                <div className="mb-8">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="flex-1 text-right">
                      <p className="text-3xl font-bold text-foreground">{prediction.homeTeam}</p>
                      <p className="text-sm text-muted-foreground mt-1">Home</p>
                    </div>
                    <p className="text-2xl font-bold text-primary">VS</p>
                    <div className="flex-1">
                      <p className="text-3xl font-bold text-foreground">{prediction.awayTeam}</p>
                      <p className="text-sm text-muted-foreground mt-1">Away</p>
                    </div>
                  </div>
                </div>

                {/* Head to Head */}
                <div className="bg-primary/5 rounded-lg p-4 border border-primary/20">
                  <p className="text-sm text-muted-foreground mb-2">Head to Head</p>
                  <p className="text-lg font-semibold text-foreground">{prediction.h2h}</p>
                </div>
              </div>

              {/* Right: Prediction Info */}
              <div className="space-y-6">
                <div>
                  <p className="text-sm text-muted-foreground mb-2">Our Prediction</p>
                  <div className="bg-primary/10 border border-primary rounded-lg p-4">
                    <p className="text-2xl font-bold text-primary">{prediction.prediction}</p>
                  </div>
                </div>

                <div>
                  <p className="text-sm text-muted-foreground mb-2">Odds</p>
                  <p className="text-3xl font-bold text-secondary">{prediction.odds}</p>
                </div>

                <div className="flex gap-4">
                  <button className="flex-1 bg-primary text-primary-foreground py-3 rounded-lg font-medium hover:bg-primary/90 transition">
                    Place Bet
                  </button>
                  <button className="flex-1 border border-border text-foreground py-3 rounded-lg font-medium hover:bg-muted transition">
                    Share
                  </button>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Ad Banner */}
          <section className="mb-8">
            <AdContainer size="horizontal" />
          </section>

          {/* Statistics Section */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-card border border-border rounded-lg p-6 text-center">
              <p className="text-sm text-muted-foreground mb-2">Confidence Level</p>
              <div className="flex items-center justify-center gap-2 mb-4">
                <div className="w-full bg-border rounded-full h-2">
                  <div className="bg-primary h-2 rounded-full" style={{ width: "82%" }}></div>
                </div>
              </div>
              <p className="text-2xl font-bold text-primary">82%</p>
            </div>

            <div className="bg-card border border-border rounded-lg p-6 text-center">
              <p className="text-sm text-muted-foreground mb-2">Typical Payout</p>
              <p className="text-3xl font-bold text-secondary">1.85x</p>
              <p className="text-sm text-muted-foreground mt-2">On $100 bet</p>
            </div>

            <div className="bg-card border border-border rounded-lg p-6 text-center">
              <p className="text-sm text-muted-foreground mb-2">Expert Consensus</p>
              <p className="text-2xl font-bold text-foreground">8 out of 10</p>
              <p className="text-sm text-muted-foreground mt-2">Experts agree</p>
            </div>
          </div>

          {/* Past Matches */}
          <div className="bg-card border border-border rounded-lg p-8 mb-8">
            <h3 className="text-2xl font-bold text-foreground mb-6">Head to Head History</h3>
            <div className="space-y-3">
              {prediction.pastMatches.map((match, index) => (
                <motion.div
                  key={index}
                  layout
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  onClick={() => setExpandedMatch(expandedMatch === index ? null : index)}
                  className="bg-muted/50 hover:bg-muted/80 rounded-lg p-4 cursor-pointer transition"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-foreground">{match.date}</p>
                      <p className="text-sm text-muted-foreground">{match.result}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-primary">{match.goals} Goals</p>
                      <p className="text-sm text-muted-foreground">
                        {match.goals === "0" ? "Low Scoring" : match.goals === "1" ? "Low Scoring" : "High Scoring"}
                      </p>
                    </div>
                  </div>
                  {expandedMatch === index && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="mt-4 pt-4 border-t border-border text-sm text-muted-foreground"
                    >
                      <p>Full-time result: {match.result}</p>
                      <p>Total goals: {match.goals}</p>
                    </motion.div>
                  )}
                </motion.div>
              ))}
            </div>
          </div>

          {/* Expert Analysis */}
          <div className="bg-card border border-border rounded-lg p-8 mb-8">
            <h3 className="text-2xl font-bold text-foreground mb-4">Expert Analysis</h3>
            <div className="space-y-4 text-muted-foreground">
              <p>
                Based on our comprehensive analysis of recent form, head-to-head records, and current team dynamics, we
                believe this prediction has strong potential.
              </p>
              <p>
                The teams have shown consistent performance in recent matches, making this one of our higher-confidence
                recommendations for this week.
              </p>
              <div className="bg-primary/5 border border-primary/20 rounded-lg p-4 mt-6">
                <p className="text-sm font-semibold text-primary mb-2">💡 Tip</p>
                <p className="text-sm text-foreground">
                  Monitor team news before match day. Injuries or tactical changes may affect the outcome.
                </p>
              </div>
            </div>
          </div>

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
