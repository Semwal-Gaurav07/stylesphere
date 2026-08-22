import React from 'react';
import { ArrowUpRight, Zap } from 'lucide-react';

export const Hero = () => {
  return (
    <section className="relative min-h-[85vh] bg-[#09090B] flex items-center justify-center overflow-hidden border-b border-white/10">
      {/* Background Lighting / Ambient Glow */}
      <div className="absolute top-1/4 -left-40 w-96 h-96 bg-blue-600/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 -right-40 w-96 h-96 bg-blue-500/10 rounded-full blur-[140px] pointer-events-none" />

      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff05_1px,transparent_1px),linear-gradient(to_bottom,#ffffff05_1px,transparent_1px)] bg-[size:4rem_4rem] pointer-events-none" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 flex flex-col items-center text-center">
        
        {/* Status Chip */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-zinc-300 text-xs font-mono tracking-widest uppercase mb-8">
          <Zap size={13} className="text-blue-500" />
          LIMITED QUANTITY DROP / EDITION 04
        </div>

        {/* Hero Title */}
        <h1 className="text-5xl sm:text-7xl lg:text-8xl font-extrabold tracking-tight uppercase text-white leading-none max-w-5xl">
          ELEVATE YOUR <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-white via-zinc-300 to-blue-500">
            STREET IDENTITY
          </span>
        </h1>

        <p className="mt-6 max-w-xl text-zinc-400 text-sm sm:text-base font-mono uppercase tracking-wider">
          Heavyweight fabrics, oversized silhouettes, and dystopian tailoring designed for modern metropolitan culture.
        </p>

        {/* CTA Buttons */}
        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <a
            href="/shop"
            className="px-8 py-4 bg-white text-black font-mono text-xs font-extrabold uppercase tracking-widest rounded-lg hover:bg-blue-500 hover:text-white transition duration-300 flex items-center gap-2 group shadow-[0_0_25px_rgba(255,255,255,0.1)] hover:shadow-[0_0_25px_rgba(59,130,246,0.4)]"
          >
            SHOP COLLECTION
            <ArrowUpRight size={16} className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
          </a>
          <a
            href="/lookbook"
            className="px-8 py-4 bg-white/5 text-zinc-300 font-mono text-xs font-bold uppercase tracking-widest rounded-lg border border-white/10 hover:bg-white/10 hover:text-white transition duration-300"
          >
            VIEW LOOKBOOK
          </a>
        </div>
      </div>
    </section>
  );
};