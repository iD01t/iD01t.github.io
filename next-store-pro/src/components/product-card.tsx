import Link from 'next/link';
import Image from 'next/image';
import type { Product } from '@/lib/schema';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';

interface ProductCardProps {
  product: Product;
  className?: string;
}

export const ProductCard = ({ product, className }: ProductCardProps) => {
  return (
    <Link href={`/products/${product.slug}`} className={cn('group block', className)}>
      <div className="overflow-hidden rounded-lg border bg-card text-card-foreground shadow-sm transition-shadow hover:shadow-md">
        <div className="relative aspect-[4/3] w-full overflow-hidden">
          <Image
<div className="overflow-hidden rounded-lg border bg-card text-card-foreground shadow-sm transition-shadow hover:shadow-md">
        <div className="relative aspect-[4/3] w-full overflow-hidden">
          <Image
            src={product.media?.length > 0 ? product.media[0] : '/images/placeholder.webp'}
            alt={product.title}
            fill
            className="object-cover transition-transform group-hover:scale-105"
            alt={product.title}
            fill
            className="object-cover transition-transform group-hover:scale-105"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
          {product.badges && (
            <div className="absolute top-2 left-2 flex gap-2">
              {product.badges.map((badgeText) => (
                <Badge key={badgeText} variant="secondary">
                  {badgeText}
                </Badge>
              ))}
            </div>
          )}
        </div>
        <div className="p-4">
          <p className="text-xs text-muted-foreground">{product.category}</p>
          <h3 className="mt-1 font-semibold leading-tight">{product.title}</h3>
          <p className="mt-2 text-sm font-medium">
            ${product.price}
            {product.compareAtPrice && (
              <span className="ml-2 text-muted-foreground line-through">
                ${product.compareAtPrice}
              </span>
            )}
          </p>
        </div>
      </div>
    </Link>
  );
};
