import React, { useState } from 'react';
import { Heart, ShoppingBag } from 'lucide-react';
import { useCartStore } from '@/store/useCartStore';

interface ProductCardProps {
  id: string;
  name: string;
  price: number;
  originalPrice?: number;
  dropTag?: string;
  category: string;
  images: [string, string];
  sizes: string[];
}

export const ProductCard: React.FC<ProductCardProps> = ({
  id,
  name,
  price,
  originalPrice,
  dropTag = 'DROP 04',
  category,
  images,
  sizes,
}) => {
  const [isWishlisted, setIsWishlisted] = useState(false);
  const [selectedSize, setSelectedSize] = useState(sizes[0] || 'M');
  const [showQuickSizes, setShowQuickSizes] = useState(false);
  const { addItem } = useCartStore();

  const handleAdd = () => {
    addItem({
      id,
      name,
      price,
      image: images[0],
      size: selectedSize,
      color: 'Matte Black',
      quantity: 1,
    });
  };

  return (
    <div className="group relative flex flex-col bg-[#121215]/80 backdrop-blur-md rounded-xl border border-white/10 hover:border-blue-500/50 transition-all duration-300 overflow-hidden">
      
      {/* Product Image Area */}
      <div className="relative aspect-[3/4] w-full overflow-hidden bg-zinc-900">
        <img
          src={images[0]}
          alt={name}
          className="h-full w-full object-cover object-center transition-transform duration-700 group-hover:scale-105 opacity-90 group-hover:opacity-100"
        />
        {images[1] && (
          <img
            src={images[1]}
            alt={`${name} detail`}
            className="absolute inset-0 h-full w-full object-cover object-center opacity-0 transition-opacity duration-500 group-hover:opacity-100"
          />
        )}

        {/* Top Badges */}
        <div className="absolute top-3 left-3 flex flex-col gap-1.5">
          <span className="bg-black/70 backdrop-blur-md text-zinc-300 font-mono text-[10px] font-bold px-2 py-0.5 rounded border border-white/10 uppercase tracking-widest">
            {dropTag}
          </span>
          {originalPrice && originalPrice > price && (
            <span className="bg-blue-600 text-white font-mono text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider">
              -{Math.round(((originalPrice - price) / originalPrice) * 100)}%
            </span>
          )}
        </div>

        {/* Wishlist Button */}
        <button
          onClick={() => setIsWishlisted(!isWishlisted)}
          className="absolute top-3 right-3 p-2 bg-black/60 backdrop-blur-md rounded-lg border border-white/10 hover:border-white/30 text-zinc-400 hover:text-white transition"
        >
          <Heart size={15} className={isWishlisted ? 'fill-blue-500 text-blue-500' : ''} />
        </button>

        {/* Quick Add Tray */}
        <div className="absolute inset-x-3 bottom-3 opacity-0 group-hover:opacity-100 transition-all duration-300">
          {showQuickSizes ? (
            <div className="bg-black/90 backdrop-blur-xl border border-white/20 rounded-lg p-2 flex items-center justify-between gap-1">
              <div className="flex gap-1 overflow-x-auto">
                {sizes.map((s) => (
                  <button
                    key={s}
                    onClick={() => {
                      setSelectedSize(s);
                      handleAdd();
                      setShowQuickSizes(false);
                    }}
                    className={`px-2.5 py-1 text-[11px] font-mono font-bold rounded ${
                      selectedSize === s
                        ? 'bg-blue-600 text-white shadow-[0_0_10px_rgba(59,130,246,0.5)]'
                        : 'bg-zinc-800 text-zinc-300 hover:bg-zinc-700'
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <button
              onClick={() => setShowQuickSizes(true)}
              className="w-full bg-white text-black py-2.5 rounded-lg text-xs font-mono font-extrabold uppercase tracking-widest flex items-center justify-center gap-2 hover:bg-blue-500 hover:text-white transition duration-200"
            >
              <ShoppingBag size={14} /> SELECT SIZE
            </button>
          )}
        </div>
      </div>

      {/* Info Section */}
      <div className="p-4 flex flex-col justify-between flex-grow">
        <div>
          <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">
            {category}
          </span>
          <h3 className="text-sm font-bold uppercase tracking-wide text-white mt-1 group-hover:text-blue-400 transition-colors">
            {name}
          </h3>
        </div>

        <div className="mt-3 flex items-center gap-2 pt-2 border-t border-white/5">
          <span className="text-base font-mono font-bold text-white">${price.toFixed(2)}</span>
          {originalPrice && (
            <span className="text-xs font-mono text-zinc-600 line-through">
              ${originalPrice.toFixed(2)}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};