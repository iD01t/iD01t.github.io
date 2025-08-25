import { describe, it, expect, vi, afterEach } from 'vitest';
import fs from 'fs/promises';
import { getProducts, getProductBySlug } from '@/lib/data';
import type { Product } from '@/lib/schema';

// Mock the entire fs/promises module
vi.mock('fs/promises');

const mockProducts: Product[] = [
  {
    id: 'prod-1',
    slug: 'product-one',
    title: 'Product One',
    description: 'Desc 1',
    price: 10,
    platform: 'Manual',
    buyUrl: '',
    media: [],
    tags: [],
    category: 'eBooks',
    releaseDate: '2024-01-01T00:00:00Z',
  },
  {
    id: 'prod-2',
    slug: 'product-two',
    title: 'Product Two',
    description: 'Desc 2',
    price: 20,
    platform: 'Manual',
    buyUrl: '',
    media: [],
    tags: [],
    category: 'Apps',
    releaseDate: '2024-02-01T00:00:00Z',
  },
];

describe('Data Fetching Utilities', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('getProducts should fetch and parse products correctly', async () => {
    // Arrange
    vi.mocked(fs.readFile).mockResolvedValue(JSON.stringify(mockProducts));

    // Act
    const products = await getProducts();

    // Assert
    expect(fs.readFile).toHaveBeenCalledWith(expect.any(String), 'utf-8');
    expect(products).toHaveLength(2);
    expect(products[0].title).toBe('Product One');
  });

  it('getProductBySlug should return the correct product', async () => {
    // Arrange
    vi.mocked(fs.readFile).mockResolvedValue(JSON.stringify(mockProducts));

    // Act
    const product = await getProductBySlug('product-two');

    // Assert
    expect(product).not.toBeNull();
    expect(product?.title).toBe('Product Two');
  });

  it('getProductBySlug should return null if product is not found', async () => {
    // Arrange
    vi.mocked(fs.readFile).mockResolvedValue(JSON.stringify(mockProducts));

    // Act
    const product = await getProductBySlug('product-three');

    // Assert
    expect(product).toBeNull();
  });

  it('getProducts should return an empty array on file read error', async () => {
    // Arrange
    vi.mocked(fs.readFile).mockRejectedValue(new Error('File not found'));

    // Act
    const products = await getProducts();

    // Assert
    expect(products).toEqual([]);
  });
});
