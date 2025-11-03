import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { PredictionCard } from "@/components/prediction-card"
import { AdContainer } from "@/components/ad-container"
import predictions from "@/data/predictions.json"

export default function PredictionsPage() {
  return (
    <>
      <Navigation />
      <main className="bg-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Header */}
          <section className="mb-12">
            <h1 className="text-4xl font-bold text-foreground mb-4">All Predictions</h1>
            <p className="text-lg text-muted-foreground mb-8">
              Expert match predictions, odds analysis, and detailed match statistics for upcoming games.
            </p>

            {/* Filter Options */}
            <div className="flex flex-wrap gap-4 mb-8">
              <button className="px-4 py-2 rounded-lg bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition">
                All Predictions
              </button>
              <button className="px-4 py-2 rounded-lg border border-border text-foreground hover:bg-muted transition">
                High Confidence
              </button>
              <button className="px-4 py-2 rounded-lg border border-border text-foreground hover:bg-muted transition">
                Today's Matches
              </button>
              <button className="px-4 py-2 rounded-lg border border-border text-foreground hover:bg-muted transition">
                This Week
              </button>
            </div>
          </section>

          {/* Ad Banner */}
          <section className="mb-8">
            <AdContainer size="horizontal" />
          </section>

          {/* Predictions Grid */}
          <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {predictions.map((prediction) => (
              <PredictionCard key={prediction.id} {...prediction} />
            ))}
          </section>

          {/* Ad Banner */}
          <section className="mb-8">
            <AdContainer size="horizontal" />
          </section>

          {/* Load More */}
          <div className="flex justify-center">
            <button className="px-8 py-3 rounded-lg border border-primary text-primary font-medium hover:bg-primary/10 transition">
              Load More Predictions
            </button>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
