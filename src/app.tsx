import React from 'react';
import { Navbar } from './components/layout/Navbar';
import { Hero } from './components/home/Hero';
import { ProductCard } from './components/product/ProductCard';
import { CartDrawer } from './components/cart/CartDrawer';

// Mock catalog for testing
const SAMPLE_PRODUCTS = [
  {
    id: 'prod-01',
    name: 'Heavyweight Cyber Hoodie',
    price: 120.00,
    originalPrice: 160.00,
    dropTag: 'DROP 04',
    category: 'Hoodies',
    images: [
      'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&q=80&w=800',
      'https://images.unsplash.com/photo-1578587018452-892bacefd3f2?auto=format&fit=crop&q=80&w=800',
    ] as [string, string],
    sizes: ['S', 'M', 'L', 'XL'],
  },
  {
    id: 'prod-02',
    name: 'Acid Wash Boxy Tee',
    price: 55.00,
    dropTag: 'LIMITED',
    category: 'T-Shirts',
    images: [
      'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&q=80&w=800',
      'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&q=80&w=800',
    ] as [string, string],
    sizes: ['M', 'L', 'XL'],
  },
  {
    id: 'prod-03',
    name: 'Tactical Parachute Cargo Pants',
    price: 140.00,
    originalPrice: 190.00,
    dropTag: 'DROP 04',
    category: 'Bottoms',
    images: [
      'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&q=80&w=800',
      'https://images.unsplash.com/photo-1517445312882-bc9910d016b7?auto=format&fit=crop&q=80&w=800',
    ] as [string, string],
    sizes: ['30', '32', '34', '36'],
  },
  {
    id: 'prod-04',
    name: 'Phantom Chunky Runners',
    price: 210.00,
    dropTag: 'EXCLUSIVE',
    category: 'Footwear',
    images: [
      'https://images.unsplash.com/photo-1552346154-21d32810aba3?auto=format&fit=crop&q=80&w=800',
      'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&q=80&w=800',
    ] as [string, string],
    sizes: ['US 8', 'US 9', 'US 10', 'US 11'],
  },
];

export default function App() {
  return (
    <div className="min-h-screen bg-[#09090B] text-zinc-100 flex flex-col font-sans">
      {/* 1. Top Navbar */}
      <Navbar />

      {/* 2. Slide-Over Cart Drawer (listens to global Zustand store) */}
      <CartDrawer />

      {/* 3. Hero Section */}
      <main className="flex-1">
        <Hero />

        {/* 4. Product Catalog Section */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="flex items-center justify-between mb-8">
            <div>
              <p className="text-xs font-mono uppercase tracking-widest text-blue-500 font-semibold">
                CURATED SELECTION
              </p>
              <h2 className="text-2xl sm:text-3xl font-extrabold uppercase tracking-tight text-white mt-1">
                LATEST RELEASES
              </h2>
            </div>
            <a
              href="/shop"
              className="text-xs font-mono tracking-widest uppercase text-zinc-400 hover:text-white transition"
            >
              VIEW ALL (24) →
            </a>
          </div>

          {/* Product Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {SAMPLE_PRODUCTS.map((product) => (
              <ProductCard key={product.id} {...product} />
            ))}
          </div>
        </section>
      </main>

      {/* 5. Minimalist Streetwear Footer */}
      <footer className="border-t border-white/10 bg-[#0D0D10] py-8 text-center text-xs font-mono text-zinc-500 uppercase tracking-widest">
        © 2026 STYLE//SPHERE LABS. ALL RIGHTS RESERVED.
      </footer>
    </div>
  );
}