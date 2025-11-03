import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { NewsCard } from "@/components/news-card"
import { AdContainer } from "@/components/ad-container"
import news from "@/data/news.json"

export default function NewsPage() {
  const featuredArticle = news[0]
  const otherArticles = news.slice(1)

  return (
    <>
      <Navigation />
      <main className="bg-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Header */}
          <section className="mb-12">
            <h1 className="text-4xl font-bold text-foreground mb-4">Football News</h1>
            <p className="text-lg text-muted-foreground">
              Stay updated with the latest news, transfers, and insights from the football world.
            </p>
          </section>

          {/* Featured Article */}
          <section className="mb-12">
            <a href={`/news/${featuredArticle.id}`} className="group block">
              <div className="bg-card border border-border rounded-lg overflow-hidden hover:shadow-lg transition-shadow h-full">
                <img
                  src={featuredArticle.thumbnail || "/placeholder.svg"}
                  alt={featuredArticle.title}
                  className="w-full h-96 object-cover group-hover:opacity-90 transition-opacity"
                />
                <div className="p-8">
                  <p className="text-sm text-muted-foreground mb-4">{featuredArticle.date}</p>
                  <h2 className="text-3xl font-bold text-foreground mb-4 group-hover:text-primary transition">
                    {featuredArticle.title}
                  </h2>
                  <p className="text-lg text-muted-foreground mb-6">{featuredArticle.summary}</p>
                  <span className="inline-flex items-center text-primary font-medium group-hover:gap-2 gap-1 transition-all">
                    Read Full Article →
                  </span>
                </div>
              </div>
            </a>
          </section>

          {/* Ad Banner */}
          <section className="mb-12">
            <AdContainer size="horizontal" />
          </section>

          {/* Category Filter */}
          <section className="mb-8">
            <div className="flex flex-wrap gap-4">
              <button className="px-4 py-2 rounded-lg bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition">
                Latest News
              </button>
              <button className="px-4 py-2 rounded-lg border border-border text-foreground hover:bg-muted transition">
                Transfers
              </button>
              <button className="px-4 py-2 rounded-lg border border-border text-foreground hover:bg-muted transition">
                Injuries & Suspensions
              </button>
              <button className="px-4 py-2 rounded-lg border border-border text-foreground hover:bg-muted transition">
                Analysis
              </button>
            </div>
          </section>

          {/* News Grid */}
          <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {otherArticles.map((article) => (
              <NewsCard key={article.id} {...article} />
            ))}
          </section>

          {/* Ad Banner */}
          <section className="mb-8">
            <AdContainer size="horizontal" />
          </section>

          {/* Load More */}
          <div className="flex justify-center">
            <button className="px-8 py-3 rounded-lg border border-primary text-primary font-medium hover:bg-primary/10 transition">
              Load More News
            </button>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
