import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { services } from '../data/content';

function formatDate(d: Date): string {
	return d.toISOString().split('T')[0] ?? d.toISOString();
}

export const GET: APIRoute = async ({ site }) => {
	const posts = (await getCollection('blog')).sort(
		(a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
	);

	const routes = [
		{ path: '/', priority: '1.0', changefreq: 'weekly' },
		{ path: '/jasa-kebersihan/', priority: '0.9', changefreq: 'weekly' },
		{ path: '/blog/', priority: '0.8', changefreq: 'weekly' },
		{ path: '/layanan/', priority: '0.9', changefreq: 'weekly' },
	];

	const serviceUrls = services.map((s) => ({
		path: `/layanan/${s.slug}/`,
		priority: '0.8',
		changefreq: 'monthly',
	}));

	const blogPostUrls = posts.map((post) => ({
		path: `/blog/${post.id}/`,
		lastmod: formatDate(post.data.pubDate),
		priority: '0.7',
		changefreq: 'monthly',
	}));

	const allUrls: { path: string; priority: string; changefreq: string; lastmod?: string }[] = [...routes, ...serviceUrls, ...blogPostUrls];

	const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allUrls
		.map(
			(url) => `	<url>
		<loc>${new URL(url.path, site).toString()}</loc>${url.lastmod ? `\n		<lastmod>${url.lastmod}</lastmod>` : ''}
		<priority>${url.priority}</priority>
		<changefreq>${url.changefreq}</changefreq>
	</url>`
		)
		.join('\n')}
</urlset>`;

	return new Response(sitemap, {
		headers: {
			'Content-Type': 'application/xml',
		},
	});
};
