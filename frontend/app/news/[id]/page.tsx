"use client"

import { motion } from "framer-motion"
import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { NewsCard } from "@/components/news-card"
import { AdContainer } from "@/components/ad-container"
import news from "@/data/news.json"

export default function NewsArticlePage({ params }: { params: { id: string } }) {
  const article = news.find((n) => n.id === params.id)
  const relatedArticles = news.filter((n) => n.id !== params.id).slice(0, 3)

  if (!article) {
    return (
      <>
        <Navigation />
        <main className="bg-background min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-foreground mb-4">Article not found</h1>
            <a href="/news" className="text-primary font-medium hover:underline">
              ← Back to News
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
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Back Button */}
          <a
            href="/news"
            className="inline-flex items-center text-primary font-medium hover:text-primary/80 transition mb-8"
          >
            ← Back to News
          </a>

          {/* Article Header */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
            <p className="text-sm text-muted-foreground mb-4">{article.date}</p>
            <h1 className="text-4xl lg:text-5xl font-bold text-foreground mb-6 leading-tight">{article.title}</h1>
            <p className="text-xl text-muted-foreground mb-8">{article.summary}</p>
          </motion.div>

          {/* Featured Image */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="mb-12 rounded-lg overflow-hidden border border-border"
          >
            <img
              src={article.thumbnail || "/placeholder.svg"}
              alt={article.title}
              className="w-full h-96 object-cover"
            />
          </motion.div>

          {/* Article Content */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="prose prose-invert max-w-none mb-12"
          >
            <div className="bg-card border border-border rounded-lg p-8 text-foreground">
              <p className="mb-6 leading-relaxed">{article.content || article.summary}</p>

              <div className="bg-primary/5 border border-primary/20 rounded-lg p-6 my-8">
                <h3 className="font-bold text-foreground mb-2">Key Points</h3>
                <ul className="list-disc list-inside space-y-2 text-muted-foreground">
                  <li>Latest developments in professional football</li>
                  <li>Impact on upcoming matches and predictions</li>
                  <li>Analysis from expert commentators</li>
                </ul>
              </div>

              <p className="leading-relaxed">
                This story continues to develop as teams and players react to recent developments. Stay tuned for
                updates and deeper analysis on how this affects the broader football landscape.
              </p>
            </div>
          </motion.div>

          {/* Article Meta */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 py-8 border-y border-border">
            <div>
              <p className="text-sm text-muted-foreground mb-1">Published</p>
              <p className="font-semibold text-foreground">{article.date}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground mb-1">Category</p>
              <p className="font-semibold text-foreground">Football News</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground mb-1">Share</p>
              <div className="flex gap-3">
                <button className="text-primary hover:text-primary/80 transition">Twitter</button>
                <button className="text-primary hover:text-primary/80 transition">Facebook</button>
              </div>
            </div>
          </div>

          {/* Ad Banner */}
          <section className="mb-12">
            <AdContainer size="horizontal" />
          </section>

          {/* Related Articles */}
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-foreground mb-8">Related News</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {relatedArticles.map((relArticle) => (
                <NewsCard key={relArticle.id} {...relArticle} />
              ))}
            </div>
          </section>

          {/* Newsletter Signup */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-r from-primary/10 to-secondary/10 border border-primary/20 rounded-lg p-8 text-center"
          >
            <h3 className="text-2xl font-bold text-foreground mb-4">Stay Updated</h3>
            <p className="text-muted-foreground mb-6">
              Get the latest football news and predictions delivered to your inbox.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-4 py-3 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition">
                Subscribe
              </button>
            </div>
          </motion.div>
        </div>
      </main>
      <Footer />
    </>
  )
}
