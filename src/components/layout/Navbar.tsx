import React, { useState } from 'react';
import { ShoppingBag, Heart, Search, Menu, X, Flame } from 'lucide-react';
import { useCartStore } from '@/store/useCartStore';

export const Navbar = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { openCart, getTotalItems } = useCartStore();
  const totalItems = getTotalItems();

  const links = [
    { name: 'DROP 04', href: '/shop?drop=04', isNew: true },
    { name: 'HOODIES', href: '/shop?category=hoodies' },
    { name: 'TEES', href: '/shop?category=tees' },
    { name: 'BOTTOMS', href: '/shop?category=bottoms' },
    { name: 'FOOTWEAR', href: '/shop?category=footwear' },
    { name: 'ARCHIVE', href: '/shop?category=archive' },
  ];

  return (
    <header className="sticky top-0 z-40 w-full bg-[#09090B]/90 backdrop-blur-xl border-b border-white/10 text-white">
      {/* Top Banner / Ticker */}
      <div className="bg-blue-600/10 border-b border-blue-500/20 py-1.5 px-4 text-center">
        <p className="text-[11px] font-mono tracking-widest text-blue-400 flex items-center justify-center gap-1.5 uppercase font-semibold">
          <Flame size={13} className="text-blue-400 animate-pulse" />
          SEASON 2026 CAPSULE // WORLDWIDE SHIPPING AVAILABLE
        </p>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between">
        
        {/* Left: Mobile Toggle & Brand Logo */}
        <div className="flex items-center gap-4">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-zinc-400 hover:text-white"
          >
            {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
          
          <a href="/" className="flex items-center gap-2 group">
            <span className="text-xl font-extrabold tracking-widest uppercase text-white group-hover:text-blue-500 transition-colors">
              STYLE<span className="text-blue-500">//</span>SPHERE
            </span>
          </a>
        </div>

        {/* Center: Navigation Links */}
        <nav className="hidden md:flex items-center gap-8">
          {links.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className="relative text-xs font-mono tracking-widest uppercase text-zinc-400 hover:text-white transition-colors duration-200"
            >
              {link.name}
              {link.isNew && (
                <span className="absolute -top-2 -right-3.5 w-1.5 h-1.5 bg-blue-500 rounded-full animate-ping" />
              )}
            </a>
          ))}
        </nav>

        {/* Right: Actions */}
        <div className="flex items-center gap-3">
          <button className="p-2.5 text-zinc-400 hover:text-white hover:bg-white/5 rounded-lg transition border border-transparent hover:border-white/10">
            <Search size={18} />
          </button>
          <button className="hidden sm:flex p-2.5 text-zinc-400 hover:text-white hover:bg-white/5 rounded-lg transition border border-transparent hover:border-white/10">
            <Heart size={18} />
          </button>
          
          {/* Neon Cart Button */}
          <button
            onClick={openCart}
            className="relative px-4 py-2 bg-blue-600 text-white rounded-lg font-mono text-xs font-bold tracking-wider uppercase flex items-center gap-2 hover:bg-blue-500 hover:shadow-[0_0_20px_rgba(59,130,246,0.5)] transition duration-300"
          >
            <ShoppingBag size={15} />
            <span className="hidden sm:inline">BAG</span>
            <span className="bg-black/40 px-1.5 py-0.5 rounded text-[10px] font-mono">
              {totalItems}
            </span>
          </button>
        </div>
      </div>
    </header>
  );
};