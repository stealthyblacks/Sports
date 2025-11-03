import { HeroCarousel } from "@/components/hero-carousel"
import { PredictionCard } from "@/components/prediction-card"
import { NewsCard } from "@/components/news-card"
import { AdContainer } from "@/components/ad-container"
import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import predictions from "@/data/predictions.json"
import news from "@/data/news.json"

export default function Home() {
  const topPredictions = predictions.slice(0, 3)
  const featuredNews = news.slice(0, 3)

  return (
    <>
      <Navigation />
      <main className="bg-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Hero Section */}
          <section className="mb-8">
            <HeroCarousel />
          </section>

          {/* Ad Banner */}
          <section className="mb-8">
            <AdContainer size="horizontal" />
          </section>

          {/* Main 3-Column Grid */}
          <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Left Column - Predictions & Ads */}
            <div className="space-y-6">
              <div className="bg-card border border-border rounded-lg p-4">
                <h3 className="font-bold text-lg mb-4 text-primary">Quick Predictions</h3>
                <div className="space-y-3">
                  {topPredictions.slice(0, 2).map((pred) => (
                    <PredictionCard key={pred.id} {...pred} />
                  ))}
                </div>
              </div>
              <AdContainer size="vertical" />
            </div>

            {/* Center Column - Featured Predictions & News */}
            <div className="space-y-6">
              <div className="bg-card border border-border rounded-lg p-4">
                <h3 className="font-bold text-lg mb-4 text-primary">Top Matches Today</h3>
                <div className="space-y-3">
                  {topPredictions.map((pred) => (
                    <PredictionCard key={pred.id} {...pred} />
                  ))}
                </div>
              </div>

              <div>
                <h3 className="font-bold text-lg mb-4 text-primary">News Flash</h3>
                <div className="space-y-4">
                  {featuredNews.map((article) => (
                    <NewsCard key={article.id} {...article} />
                  ))}
                </div>
              </div>
            </div>

            {/* Right Column - Stacked Ads */}
            <div className="space-y-6">
              <AdContainer size="vertical" />
              <AdContainer size="vertical" />
              <div className="bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20 rounded-lg p-6 text-center">
                <h4 className="font-bold text-primary mb-2">Special Offer</h4>
                <p className="text-sm text-foreground mb-4">Get access to premium predictions and expert analysis.</p>
                <button className="bg-primary text-primary-foreground px-6 py-2 rounded-lg font-medium hover:bg-primary/90 transition">
                  Learn More
                </button>
              </div>
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </>
  )
}
