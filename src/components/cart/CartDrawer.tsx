import React from 'react';
import { X, Trash2, ArrowRight, ShieldCheck } from 'lucide-react';
import { useCartStore } from '@/store/useCartStore';

export const CartDrawer = () => {
  const { items, isOpen, closeCart, removeItem, updateQuantity, getTotalPrice } = useCartStore();
  const subtotal = getTotalPrice();
  const freeShippingThreshold = 150;
  const progress = Math.min((subtotal / freeShippingThreshold) * 100, 100);
  const amountNeeded = (freeShippingThreshold - subtotal).toFixed(2);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Dimmed backdrop */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-md transition-opacity"
        onClick={closeCart}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-[#09090B] border-l border-white/10 shadow-2xl flex flex-col text-white">
          
          {/* Header */}
          <div className="px-6 py-5 border-b border-white/10 flex items-center justify-between">
            <h2 className="text-sm font-mono uppercase tracking-widest font-extrabold text-white">
              SHOPPING BAG // ({items.length})
            </h2>
            <button
              onClick={closeCart}
              className="p-1.5 text-zinc-400 hover:text-white hover:bg-white/5 rounded-lg border border-transparent hover:border-white/10"
            >
              <X size={18} />
            </button>
          </div>

          {/* Tiered Free Shipping Status */}
          <div className="bg-white/5 px-6 py-3.5 border-b border-white/10">
            <p className="text-xs font-mono text-zinc-300 uppercase tracking-wider">
              {progress >= 100 ? (
                <span className="text-blue-400 font-bold">UNLOCKED FREE GLOBAL EXPRESS</span>
              ) : (
                <>ADD <span className="text-white font-bold">${amountNeeded}</span> FOR FREE EXPRESS</>
              )}
            </p>
            <div className="w-full bg-zinc-800 h-1 rounded-full mt-2 overflow-hidden">
              <div
                className="bg-blue-500 h-full rounded-full transition-all duration-500 shadow-[0_0_8px_rgba(59,130,246,0.8)]"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Cart Item Feed */}
          <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4 divide-y divide-white/5">
            {items.length === 0 ? (
              <div className="text-center py-20">
                <p className="font-mono text-xs uppercase tracking-widest text-zinc-500">
                  NO ITEMS REGISTERED IN BAG
                </p>
                <button
                  onClick={closeCart}
                  className="mt-4 px-6 py-2.5 bg-white text-black font-mono text-xs font-bold uppercase tracking-widest rounded-lg hover:bg-blue-500 hover:text-white transition"
                >
                  BROWSE RELEASES
                </button>
              </div>
            ) : (
              items.map((item) => (
                <div key={`${item.id}-${item.size}`} className="pt-4 flex gap-4">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-20 h-24 object-cover rounded-lg bg-zinc-900 border border-white/10"
                  />
                  <div className="flex-1 flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-start">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-white">
                          {item.name}
                        </h4>
                        <button
                          onClick={() => removeItem(item.id, item.size)}
                          className="text-zinc-500 hover:text-rose-500 transition"
                        >
                          <Trash2 size={15} />
                        </button>
                      </div>
                      <p className="text-[11px] font-mono text-zinc-400 mt-1">SIZE: {item.size}</p>
                      <p className="text-sm font-mono font-bold text-white mt-1">
                        ${item.price.toFixed(2)}
                      </p>
                    </div>

                    {/* Quantity Stepper */}
                    <div className="flex items-center gap-2 border border-white/10 w-fit rounded-md px-2 py-0.5 bg-zinc-900">
                      <button
                        onClick={() => updateQuantity(item.id, item.size, -1)}
                        className="text-zinc-400 hover:text-white text-xs px-1"
                      >
                        -
                      </button>
                      <span className="text-xs font-mono font-bold px-2">{item.quantity}</span>
                      <button
                        onClick={() => updateQuantity(item.id, item.size, 1)}
                        className="text-zinc-400 hover:text-white text-xs px-1"
                      >
                        +
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer Checkout Trigger */}
          {items.length > 0 && (
            <div className="border-t border-white/10 px-6 py-5 space-y-4 bg-[#0D0D10]">
              <div className="flex justify-between items-center text-sm font-mono">
                <span className="text-zinc-400 uppercase tracking-wider">SUBTOTAL</span>
                <span className="text-lg font-bold text-white">${subtotal.toFixed(2)}</span>
              </div>
              <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-widest flex items-center gap-1.5">
                <ShieldCheck size={14} className="text-blue-500" /> ENCRYPTED SECURE CHECKOUT
              </p>
              <a
                href="/checkout"
                className="w-full bg-blue-600 text-white py-3.5 rounded-lg font-mono text-xs font-extrabold tracking-widest uppercase flex items-center justify-center gap-2 hover:bg-blue-500 hover:shadow-[0_0_20px_rgba(59,130,246,0.5)] transition duration-300"
              >
                PROCEED TO CHECKOUT <ArrowRight size={15} />
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};