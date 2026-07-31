export interface Service {
	slug: string;
	title: string;
	headline: string;
	description: string;
	image: string;
	body: string;
	useCases?: { title: string; desc: string }[];
	areas?: string[];
	includes: string[];
	addOns?: string[];
	notIncludes?: string[];
	requirements?: string[];
	faq: Faq[];
	ctaMsg: string;
	tnc?: string[];
	internalLinks?: { label: string; href: string }[];
}

export interface Situation {
	img: string;
	title: string;
	body: string;
	cta: string;
	msg: string;
	badge?: string;
	slug?: string;
}

export interface Reason {
	emoji: string;
	title: string;
	body: string;
}

export interface Step {
	n: string;
	title: string;
	body: string;
}

export interface Review {
	name: string;
	area: string;
	text: string;
}

export interface Faq {
	q: string;
	a: string;
}

export const services: Service[] = [
	{
		slug: 'after-renovasi',
		title: 'After Renovasi',
		headline: 'Rumah Bersih Setelah Renovasi — Siap Ditempati',
		description: 'Layanan cleaning pasca renovasi untuk membersihkan debu semen, sisa cat, dan kotoran berat agar rumah Anda siap ditempati.',
		image: '/renovasi.png',
		body: 'Renovasi meninggalkan banyak debu halus, sisa semen, dan bekas cat di sudut-sudut yang sulit dijangkau. Tim Tentram membersihkan dari plafon hingga lantai, termasuk area tersembunyi seperti kusen jendela, celah AC, dan belakang furnitur. Hasilnya: rumah benar-benar bersih dan nyaman untuk ditempati.',
		includes: [
			'Pembersihan debu halus dan sisa semen',
			'Pembersihan plafon, dinding, dan lantai',
			'Pembersihan kusen, jendela, dan celah AC',
			'Pembersihan area tersembunyi di belakang furnitur',
			'Quality checklist sebelum serah terima',
		],
		notIncludes: [
			'Pengangkutan material renovasi besar (batu bata, kayu, dll)',
			'Pembersihan tumpukan sampah konstruksi',
			'Perbaikan atau pengecatan ulang',
		],
		faq: [
			{ q: 'Berapa lama cleaning pasca renovasi?', a: 'Tergantung luas rumah dan tingkat kekotoran. Untuk rumah standar biasanya 1–2 hari kerja.' },
			{ q: 'Apakah tim membawa peralatan sendiri?', a: 'Ya, tim kami datang lengkap dengan peralatan dan cleaning agent yang aman.' },
			{ q: 'Apakah bisa ditangani dalam sehari?', a: 'Bisa untuk apartemen atau rumah kecil. Estimasi pasti diberikan setelah survey.' },
		],
		ctaMsg: 'Halo Tentram, saya ingin bertanya tentang layanan cleaning. [Web]',
		internalLinks: [
			{ label: '5 Tips Rumah Bersih Setelah Renovasi', href: '/blog/5-tips-rumah-bersih-setelah-renovasi/' },
			{ label: 'Kapan Waktu Tepat Deep Cleaning?', href: '/blog/kapan-waktu-tepat-deep-cleaning/' },
		],
	},
	{
		slug: 'move-in',
		title: 'Move In Cleaning',
		headline: 'Masuk Rumah Baru dalam Keadaan Bersih',
		description: 'Move in cleaning untuk rumah dan apartemen baru sebelum Anda mulai menempati setiap sudut dengan higienis.',
		image: '/Pindahan.png',
		body: 'Mulai tinggal di rumah baru dengan benar-benar bersih. Layanan move in cleaning kami membersihkan sisa debu konstruksi, noda di lantai dan dinding, serta kamar mandi dan dapur hingga higienis. Ideal untuk rumah baru, apartemen baru, atau rumah bekas kontrakan.',
		includes: [
			'Pembersihan seluruh ruangan dari debu dan kotoran',
			'Pembersihan kamar mandi dan dapur secara detail',
			'Pembersihan lemari, rak, dan permukaan',
			'Pembersihan lantai, dinding, dan plafon',
			'Quality checklist sebelum serah terima',
		],
		notIncludes: [
			'Packing dan unpacking barang pindahan',
			'Pengangkutan sampah pindahan besar',
			'Pembersihan area luar rumah/lapangan parkir',
		],
		faq: [
			{ q: 'Kapan sebaiknya booking move in cleaning?', a: 'Setelah seluruh barang renovasi/bangunan dibersihkan dan sebelum furniture masuk.' },
			{ q: 'Apakah aman untuk lantai dan permukaan baru?', a: 'Ya, kami menggunakan cleaning agent yang aman dan tidak merusak permukaan.' },
			{ q: 'Berapa lama prosesnya?', a: 'Apartemen 2–4 jam, rumah standar 4–8 jam tergantung luas.' },
		],
		ctaMsg: 'Halo Tentram, saya ingin bertanya tentang layanan cleaning. [Web]',
		internalLinks: [
			{ label: 'Tips Pindahan Rumah Bersih', href: '/blog/tips-pindahan-rumah-bersih/' },
			{ label: 'Apa Itu Deep Cleaning?', href: '/blog/apa-itu-deep-cleaning/' },
			{ label: 'Home Cleaning vs Deep Cleaning', href: '/blog/home-cleaning-vs-deep-cleaning/' },
		],
	},
	{
		slug: 'home-cleaning',
		title: 'Home Cleaning',
		headline: 'Rumah Bersih Tanpa Anda Harus Capek Sendiri',
		description: 'Layanan home cleaning rutin untuk rumah dan apartemen di Jakarta, BSD, Tangerang, Bekasi, dan sekitarnya.',
		image: '/rumah.png',
		body: 'Home cleaning adalah layanan pembersihan rutin untuk menjaga rumah atau apartemen tetap nyaman setiap hari. Tim kami membersihkan area umum, kamar tidur, kamar mandi, dan dapur sesuai jadwal yang Anda pilih. Cocok untuk keluarga sibuk, profesional, atau siapa pun yang ingin rumah selalu rapi tanpa repot.',
		includes: [
			'Pembersihan debu pada permukaan dan furniture',
			'Pembersihan lantai (vacuum + mop)',
			'Pembersihan kamar mandi dan wastafel',
			'Pembersihan dapur ringan',
			'Penataan ruangan umum dan kamar tidur',
		],
		addOns: [
			'Cuci + setrika pakaian',
			'Cuci AC',
			'Hydro cleaning sofa/kasur/karpet',
		],
		faq: [
			{ q: 'Apakah layanan ini harus rutin tiap minggu?', a: 'Tidak harus. Anda bisa pilih frekuensi mingguan, bulanan, atau sesuai kebutuhan.' },
			{ q: 'Saya punya hewan peliharaan, apakah aman?', a: 'Ya, kami menggunakan produk yang aman untuk hewan peliharaan. Beritahu kami saat booking.' },
			{ q: 'Apakah saya harus ada di rumah?', a: 'Tidak harus. Banyak pelanggan memberikan instruksi dan akses saat cleaning.' },
		],
		ctaMsg: 'Halo Tentram, saya ingin bertanya tentang layanan cleaning. [Web]',
		internalLinks: [
			{ label: 'Home Cleaning vs Deep Cleaning', href: '/blog/home-cleaning-vs-deep-cleaning/' },
			{ label: 'Kenapa Harus Pakai Home Cleaning Service', href: '/blog/kenapa-harus-pakai-home-cleaning-service/' },
			{ label: 'Harga Cleaning Service Jakarta', href: '/blog/harga-cleaning-service-jakarta/' },
		],
	},
	{
		slug: 'office-cleaning',
		title: 'Office Cleaning',
		headline: 'Kantor Bersih untuk Tim dan Pelanggan Anda',
		description: 'Jasa office cleaning harian atau berkala untuk kantor, coworking space, dan ruang kerja di Jakarta dan sekitarnya.',
		image: '/kantor.png',
		body: 'Kantor yang bersih menciptakan lingkungan kerja yang lebih nyaman dan produktif. Kami melayani office cleaning harian maupun berkala untuk area kerja, meeting room, pantry, toilet, dan lobby. Jadwal fleksibel, bisa di luar jam kantor agar tidak mengganggu aktivitas.',
		includes: [
			'Pembersihan area kerja dan meja',
			'Pembersihan lantai (vacuum + mop)',
			'Pembersihan toilet dan pantry',
			'Pengosongan tempat sampah',
			'Penataan ruang meeting dan lobby',
		],
		addOns: [
			'Disinfection fogging',
			'Window/glass cleaning',
			'Cuci karpet kantor',
		],
		faq: [
			{ q: 'Apakah bisa dilakukan di luar jam kantor?', a: 'Ya, kami bisa jadwalkan sore, malam, atau akhir pekan.' },
			{ q: 'Apakah harus kontrak jangka panjang?', a: 'Tidak harus. Bisa trial satu kali, mingguan, atau kontrak bulanan.' },
			{ q: 'Berapa besar kantor yang bisa ditangani?', a: 'Dari kantor kecil hingga gedung multi-lantai. Estimasi disesuaikan setelah survey.' },
		],
		ctaMsg: 'Halo Tentram, saya ingin bertanya tentang layanan cleaning. [Web]',
		internalLinks: [
			{ label: 'Harga Cleaning Service Jakarta', href: '/blog/harga-cleaning-service-jakarta/' },
			{ label: 'Deep Cleaning Jakarta Proses dan Harga', href: '/blog/deep-cleaning-jakarta-proses-dan-harga/' },
		],
	},
	{
		slug: 'deep-cleaning',
		title: 'Deep Cleaning',
		headline: 'Pembersihan Menyeluruh untuk Rumah yang Siap Ditempati',
		description: 'Deep cleaning menyeluruh untuk pindahan, renovasi, dan gudang. Tim profesional Tentram bersihkan area yang terlewat: kerak kamar mandi, debu balik furniture, noda dinding.',
		image: '/deepcleantoilet.png',
		body: 'Deep cleaning adalah pembersihan menyeluruh dan mendetail, khususnya bagian dalam ruangan. Berbeda dari cleaning rutin yang hanya merawat permukaan, deep cleaning menjangkau area yang jarang tersentuh — debu di balik dan bawah furniture, kerak serta jamur di kamar mandi, noda di dinding dan kusen, hingga sudut-sudut yang terlewat.',
		useCases: [
			{ title: '🏠 Pindahan (Move In / Move Out)', desc: 'Rumah baru atau lama perlu dibersihkan menyeluruh sebelum ditempati. Kami pastikan setiap sudut siap huni.' },
			{ title: '🔨 Selesai Renovasi', desc: 'Debu renovasi menempel di mana-mana — langit-langit, balok jendela, celah keramik. Deep cleaning hilangkan semua jejak.' },
			{ title: '📦 Cleaning Gudang', desc: 'Gudang yang berdebu dan berantakan mengganggu produktivitas. Kami bersihkan dari atas hingga bawah.' },
		],
		areas: ['Ruang Tamu', 'Kamar Tidur', 'Dapur', 'Gudang', 'Tangga', 'Furniture', 'Pintu, Jendela & Kaca', 'Kamar Mandi', 'Balkon'],
		includes: [
			'Pembersihan detail area tersembunyi',
			'Pembersihan kerak dan jamur kamar mandi',
			'Pembersihan noda dinding, kusen, dan plafon',
			'Pembersihan di dalam dan luar lemari/rak',
			'Vacuum menyeluruh termasuk sudut dan celah',
		],
		addOns: [
			'Hydro cleaning sofa/kasur/karpet',
			'Cuci AC',
			'Disinfection fogging',
		],
		notIncludes: [
			'Pembersihan ketinggian tanpa alat safety',
			'Memindahkan barang-barang berat',
			'Perbaikan furniture atau komponen yang rusak',
			'Taman dan area parkir dengan jet spray',
			'Lantai marmer dan granit',
		],
		requirements: [
			'Luas bangunan minimal 35 m² (di bawah 35 m² penyesuaian harga)',
			'Informasi luas bangunan per lantai',
			'Jumlah tingkatan lantai yang akan di-deep cleaning',
			'Video detail setiap area yang akan dibersihkan',
			'DP 50% sebelum pengerjaan dimulai',
		],
		faq: [
			{ q: 'Apa bedanya deep cleaning dan home cleaning?', a: 'Home cleaning merawat kebersihan harian atau berkala. Deep cleaning adalah pembersihan menyeluruh dan mendetail — menjangkau area yang tidak terjangkau oleh cleaning rutin, seperti balik furniture, celah keramik, dan langit-langit.' },
			{ q: 'Kapan saya butuh deep cleaning?', a: 'Saat pindah rumah (move in/move out), setelah renovasi, atau saat gudang perlu dibersihkan menyeluruh. Bukan untuk kebersihan harian.' },
			{ q: 'Seberapa sering harus deep cleaning?', a: 'Tidak seperti cleaning rutin, deep cleaning dilakukan sesuai kebutuhan — saat pindahan, renovasi, atau kondisi bangunan sudah sangat kotor. Bukan jadwal bulanan.' },
			{ q: 'Berapa lama prosesnya?', a: 'Rumah standar biasanya 4–8 jam. Luas bangunan dan tingkat kekotoran menentukan estimasi waktu.' },
			{ q: 'Apakah ada minimal luas bangunan?', a: 'Ya, minimal 35 m². Untuk bangunan di bawah 35 m² berlaku penyesuaian harga. Untuk bangunan >150 m² dikenakan biaya survey Rp50.000.' },
			{ q: 'Apa yang perlu saya siapkan sebelum pengerjaan?', a: 'Informasi luas bangunan per lantai, jumlah lantai, dan video detail area yang akan dibersihkan. Also pastikan tidak ada pengerjaan lain yang berjalan bersamaan di lokasi yang sama.' },
			{ q: 'Area mana saja yang masuk cakupan?', a: 'Ruang Tamu, Kamar Tidur, Dapur, Gudang, Tangga, Furniture, Pintu/Jendela/Kaca, Kamar Mandi, dan Balkon.' },
			{ q: 'Apa yang tidak termasuk dalam deep cleaning?', a: 'Pembersihan ketinggian tanpa alat safety, memindahkan barang berat, perbaikan furniture, taman/area parkir dengan jet spray, serta lantai marmer dan granit.' },
		],
		ctaMsg: 'Halo Tentram, saya ingin bertanya tentang layanan cleaning. [Web]',
		tnc: [
			'Deep Cleaning adalah pembersihan menyeluruh dan mendetail (khususnya bagian dalam ruangan). Diperuntukkan bagi bangunan yang akan ditempati (move in/move out), selesai renovasi, dan gudang.',
			'Jam operasional Deep Cleaning: 09:00 – 19:00 WIB.',
			'Luas bangunan minimal 35 m². Untuk luas di bawah 35 m² berlaku penyesuaian harga.',
			'Pengerjaan baru dilakukan setelah customer membayar DP sebesar 50%.',
			'Untuk luas bangunan >150 m² dikenakan biaya survey sebesar Rp50.000.',
			'Customer WAJIB memberikan informasi: luas bangunan per lantai, jumlah tingkatan lantai, dan video detail setiap area yang akan di-deep cleaning.',
			'Dalam satu lokasi tidak boleh ada pengerjaan lain yang bersamaan, karena akan mengganggu hasil pembersihan.',
			'Cakupan area: Ruang Tamu, Kamar Tidur, Dapur, Gudang, Tangga, Furniture, Pintu/Jendela/Kaca, Kamar Mandi, Balkon.',
			'Yang TIDAK termasuk cakupan: pembersihan ketinggian tanpa alat safety, memindahkan barang berat, perbaikan furniture/rusak, taman dan area parkir dengan jet spray, lantai marmer dan granit.',
			'Pengerjaan menggunakan cairan pembersih dan alat khusus dari Tentram. Jika customer menggunakan chemical sendiri, Tentram tidak bertanggung jawab atas kerusakan.',
			'Customer wajib melakukan pengecekan setelah petugas selesai, untuk memastikan sesuai orderan dan mengantisipasi komplain.',
			'Pemesanan langsung kepada petugas tanpa melalui Tentram tidak dapat diklaim dan Tentram tidak bertanggung jawab.',
		],
		internalLinks: [
			{ label: 'Perbedaan Deep Cleaning vs Home Cleaning', href: '/blog/home-cleaning-vs-deep-cleaning/' },
			{ label: 'Tips Pindahan Rumah Bersih', href: '/blog/tips-pindahan-rumah-bersih/' },
			{ label: 'Harga Cleaning Service Jakarta', href: '/blog/harga-cleaning-service-jakarta/' },
		],
	},
	{
		slug: 'hydro-cleaning',
		title: 'Hydro Cleaning',
		headline: 'Sofa, Kasur, dan Karpet Bersih dari Dalam',
		description: 'Hydro cleaning menggunakan teknologi hydro extraction untuk membersihkan sofa, kasur, karpet, dan interior kain secara mendalam.',
		image: '/HydroCleaning.png',
		body: 'Sofa, kasur, dan karpet menyimpan debu, tungau, noda, dan bau di dalam serat kain. Vacuum biasa hanya membersihkan permukaan. Hydro cleaning kami menyemprotkan cairan pembersih hangat bertekanan lalu menyedotnya kembali beserta kotoran dari dalam serat. Hasilnya lebih higienis dan tahan lama.',
		includes: [
			'Pembersihan sofa, kasur, atau karpet',
			'Hydro extraction tekanan hangat',
			'Penghilangan noda dan bau tidak sedap',
			'Pengeringan cepat',
			'Quality check sebelum serah terima',
		],
		notIncludes: [
			'Perbaikan robekan atau kerusakan fabric',
			'Pembersihan bantal isian bulu/lateks yang tidak boleh basah',
			'Penghilangan noda permanen (tinta, cat, dll) tanpa jaminan',
		],
		faq: [
			{ q: 'Berapa lama kering setelah hydro cleaning?', a: 'Biasanya 2–6 jam tergantung ventilasi dan cuaca.' },
			{ q: 'Apakah aman untuk sofa kulit?', a: 'Hydro cleaning khusus untuk fabric. Untuk kulit kami menggunakan metode yang berbeda, silakan konsultasikan.' },
			{ q: 'Seberapa sering perlu hydro cleaning?', a: 'Untuk rumah normal 4–6 bulan, untuk rumah dengan anak/peliharaan 2–3 bulan.' },
		],
		ctaMsg: 'Halo Tentram, saya ingin bertanya tentang layanan cleaning. [Web]',
		internalLinks: [
			{ label: 'Merawat Sofa Karpet Hydro Cleaning', href: '/blog/merawat-sofa-karpet-hydro-cleaning/' },
			{ label: 'Harga Cleaning Service Jakarta', href: '/blog/harga-cleaning-service-jakarta/' },
		],
	},
	{
		slug: 'cuci-ac',
		title: 'Cuci AC',
		headline: 'AC Dingin, Bersih, dan Bebas Bau',
		description: 'Layanan cuci AC rumah dan kantor oleh tim profesional tanpa perlu Anda bongkar sendiri.',
		image: '/cuci-ac.png',
		body: 'AC yang jarang dibersihkan bisa mengurangi pendinginan, meningkatkan listrik, dan menyebarkan debu serta bau. Layanan cuci AC Tentram membersihkan filter, evaporator, blower, dan bagian dalam unit AC tanpa perlu Anda repot. Hasilnya AC lebih dingin, lebih hemat, dan udara lebih segar.',
		includes: [
			'Pembersihan filter AC',
			'Pembersihan evaporator dan blower',
			'Pembersihan drainase',
			'Pengecekan freon dan tekanan',
			'Laporan kondisi AC',
		],
		addOns: [
			'Tambah freon',
			'Service kompresor',
			'Pembersihan ducting AC central',
		],
		faq: [
			{ q: 'Berapa lama proses cuci AC?', a: 'Satu unit AC biasanya 45–90 menit.' },
			{ q: 'Seberapa sering AC harus dicuci?', a: 'Rekomendasi 3–6 bulan sekali untuk pemakaian normal.' },
			{ q: 'Apakah harus ada di rumah saat pengerjaan?', a: 'Ya, minimal untuk memberikan akses ke unit AC. Pengerjaan diawasi oleh tim.' },
		],
		ctaMsg: 'Halo Tentram, saya ingin bertanya tentang layanan cleaning. [Web]',
		internalLinks: [
			{ label: 'Harga Cleaning Service Jakarta', href: '/blog/harga-cleaning-service-jakarta/' },
		],
	},
	{
		slug: 'cleaning-gudang',
		title: 'Cleaning Gudang',
		headline: 'Gudang Rapi, Bersih, dan Aman Digunakan',
		description: 'Layanan cleaning gudang untuk membersihkan debu, tumpukan kotoran, dan sisa material agar gudang kembali rapi.',
		image: '/gudang.png',
		body: 'Gudang yang terbengkalai sering menumpuk debu, kotoran, dan sisa material yang mengganggu aktivitas operasional. Tim Tentram membersihkan lantai, rak, lorong, dan area penyimpanan dengan peralatan yang sesuai. Hasilnya gudang lebih rapi, aman, dan nyaman untuk bekerja.',
		includes: [
			'Pembersihan lantai dan lorong gudang',
			'Pembersihan debu di rak dan penyimpanan',
			'Pengosongan sampah ringan',
			'Penataan area penyimpanan (jika diminta)',
			'Quality checklist area luas',
		],
		notIncludes: [
			'Pengangkutan barang berat/sisa material besar',
			'Pengoperasian forklift atau alat berat',
			'Perbaikan struktur gudang',
		],
		faq: [
			{ q: 'Berapa lama cleaning gudang?', a: 'Tergantung luas dan kondisi gudang. Estimasi diberikan setelah survey.' },
			{ q: 'Apakah tim membantu menata barang?', a: 'Bisa, asalkan disepakati sebelum pengerjaan.' },
			{ q: 'Apakah perlu listrik/air di gudang?', a: 'Idealnya ya, agar pembersihan maksimal. Jika terbatas, tim akan menyesuaikan.' },
		],
		ctaMsg: 'Halo Tentram, saya ingin bertanya tentang layanan cleaning. [Web]',
		internalLinks: [
			{ label: 'Deep Cleaning Jakarta Proses dan Harga', href: '/blog/deep-cleaning-jakarta-proses-dan-harga/' },
			{ label: 'Kapan Waktu Tepat Deep Cleaning?', href: '/blog/kapan-waktu-tepat-deep-cleaning/' },
		],
	},
	{
		slug: 'cleaning-kamar-mandi',
		title: 'Cleaning Kamar Mandi',
		headline: 'Kamar Mandi Kinclong dan Bebas Jamur',
		description: 'Layanan khusus pembersihan kamar mandi: hilangkan kerak, jamur, noda, dan bau tidak sedap secara detail.',
		image: '/kamar-mandi.png',
		body: 'Kamar mandi adalah area yang paling cepat mengumpulkan kerak, jamur, dan bau. Layanan ini membersihkan seluruh permukaan keramik, kloset, wastafel, shower, kaca, dan area sela-sela yang sering terlewat. Cocok untuk kamar mandi rumah, apartemen, kost, atau kamar mandi kantor.',
		includes: [
			'Pembersihan kerak dan noda keramik',
			'Pembersihan jamur di sela-sela',
			'Pembersihan kloset, wastafel, dan shower',
			'Pembersihan kaca dan cermin',
			'Penghilangan bau tidak sedap',
		],
		addOns: [
			'Pembersihan talang/air kotoran',
			'Poles keramik untuk kilau tambahan',
		],
		faq: [
			{ q: 'Apakah aman untuk keramik dan kloset?', a: 'Ya, kami menggunakan cleaning agent yang aman dan tidak merusak permukaan.' },
			{ q: 'Berapa lama prosesnya?', a: 'Satu kamar mandi biasanya 1–2 jam. Lebih banyak unit akan memakan waktu lebih lama.' },
			{ q: 'Apakah bisa untuk kamar mandi kantor/kost?', a: 'Bisa, kami melayani kamar mandi di berbagai jenis properti.' },
		],
		ctaMsg: 'Halo Tentram, saya ingin bertanya tentang layanan cleaning. [Web]',
		internalLinks: [
			{ label: 'Apa Itu Deep Cleaning?', href: '/blog/apa-itu-deep-cleaning/' },
			{ label: 'Harga Cleaning Service Jakarta', href: '/blog/harga-cleaning-service-jakarta/' },
		],
	},
];

export const situations: Situation[] = [
	{ img: '/renovasi.png', title: 'After Renovasi', body: 'Dibuangi debu, sisa semen, dan bekas cat hingga siap ditempati.', cta: 'Saya baru renovasi', msg: 'Halo Tentram, saya baru selesai renovasi rumah dan butuh pembersihan. Boleh minta penawaran?', slug: 'after-renovasi' },
	{ img: '/Pindahan.png', title: 'Baru Pindahan', body: 'Setiap sudut dibersihkan sebelum Anda mulai menempati.', cta: 'Saya baru pindahan', msg: 'Halo Tentram, saya baru pindah rumah dan ingin move in cleaning. Boleh minta penawaran?', slug: 'move-in' },
	{ img: '/rumah.png', title: 'Rumah Terasa Kotor', body: 'Tidak sempat membersihkan sendiri? Biarkan kami membantu.', cta: 'Saya butuh home cleaning', msg: 'Halo Tentram, saya butuh home cleaning untuk rumah saya. Boleh minta penawaran?', slug: 'home-cleaning' },
	{ img: '/kantor.png', title: 'Office Cleaning', body: 'Lingkungan kerja yang lebih nyaman untuk tim dan pelanggan.', cta: 'Saya butuh office cleaning', msg: 'Halo Tentram, kantor kami butuh cleaning rutin/berkala. Boleh minta penawaran?', slug: 'office-cleaning' },
	{ img: '/deepcleantoilet.png', title: 'Deep Cleaning', body: 'Pembersihan menyeluruh hingga area yang jarang dibersihkan.', cta: 'Lihat deep cleaning', msg: 'Halo Tentram, saya tertarik dengan layanan Deep Cleaning. Boleh minta penawaran?', slug: 'deep-cleaning' },
	{ img: '/HydroCleaning.png', title: 'Hydro Cleaning', body: 'Cuci sofa, kasur, dan karpet dengan teknologi hydro extraction.', cta: 'Lihat hydro cleaning', msg: 'Halo Tentram, saya tertarik dengan layanan Hydro Cleaning (cuci sofa/kasur/karpet). Boleh minta penawaran?', slug: 'hydro-cleaning' },
	{ img: '/cuci-ac.png', title: 'Cuci AC', body: 'AC dingin maksimal dan bebas bau tanpa perlu bongkar sendiri.', cta: 'Saya butuh cuci AC', msg: 'Halo Tentram, saya butuh layanan cuci AC. Boleh minta penawaran?', slug: 'cuci-ac', badge: 'Baru' },
	{ img: '/gudang.png', title: 'Cleaning Gudang', body: 'Bersihkan debu dan kotoran menumpuk agar gudang rapi dan aman digunakan.', cta: 'Saya butuh cleaning gudang', msg: 'Halo Tentram, saya butuh layanan cleaning gudang. Boleh minta penawaran?', slug: 'cleaning-gudang' },
	{ img: '/kamar-mandi.png', title: 'Cleaning Kamar Mandi', body: 'Hilangkan kerak, jamur, dan bau tak sedap hingga kamar mandi kembali kinclong.', cta: 'Saya butuh cleaning kamar mandi', msg: 'Halo Tentram, saya butuh layanan cleaning kamar mandi. Boleh minta penawaran?', slug: 'cleaning-kamar-mandi' },
];

export const reasons: Reason[] = [
	{ emoji: '📅', title: 'Bisa Pilih Jadwal', body: 'Atur waktu cleaning sesuai jadwal Anda.' },
	{ emoji: '🧑‍🤝‍🧑', title: 'Bisa Pilih Mitra', body: 'Pilih mitra cleaning kepercayaan Anda.' },
	{ emoji: '🔄', title: 'Bisa Reschedule', body: 'Ubah jadwal dengan mudah tanpa ribet.' },
	{ emoji: '💳', title: 'Bisa Bayar Pakai Apa Aja', body: 'Berbagai metode pembayaran didukung.' },
];

export const steps: Step[] = [
	{ n: '1', title: 'Hubungi WhatsApp', body: 'Chat tim kami, fast response.' },
	{ n: '2', title: 'Ceritakan kebutuhan Anda', body: 'Jelaskan situasi rumah atau kantor.' },
	{ n: '3', title: 'Terima estimasi', body: 'Estimasi harga transparan.' },
	{ n: '4', title: 'Tim datang', body: 'Tim profesional datang sesuai jadwal.' },
	{ n: '5', title: 'Rumah kembali bersih', body: 'Nikmati hasilnya, siap digunakan.' },
];

export const reviews: Review[] = [
	{ name: 'Dewi A.', area: 'BSD', text: 'Baru pindah dan rumah langsung bersih maksimal. Timnya teliti banget.' },
	{ name: 'Reza P.', area: 'Jakarta Selatan', text: 'Setelah renovasi parah debunya. Tentram beresin sampai bersih, siap ditempati.' },
	{ name: 'Sinta M.', area: 'Gading Serpong', text: 'Pakai layanan rutin. Selalu tepat waktu dan hasilnya konsisten.' },
];

export const areas: string[] = [
	'Jakarta Selatan', 'Jakarta Barat', 'Jakarta Utara', 'Jakarta Timur', 'BSD City', 'Gading Serpong', 'Alam Sutera', 'Bintaro', 'Tangerang', 'Bekasi',
];

export const faqs: Faq[] = [
	{ q: 'Apakah tim membawa alat sendiri?', a: 'Ya. Tim Tentram datang dengan peralatan lengkap, Anda tidak perlu menyiapkan apa pun.' },
	{ q: 'Berapa lama proses cleaning?', a: 'Tergantung luas dan kondisi ruangan. Home cleaning biasanya 3–5 jam, deep cleaning bisa lebih lama. Estimasi pasti diberikan saat booking.' },
	{ q: 'Bagaimana menentukan harga?', a: 'Harga disesuaikan dengan luas area, jenis layanan, dan kondisi. Semua transparan, tanpa biaya tersembunyi.' },
	{ q: 'Apakah bisa datang di akhir pekan?', a: 'Bisa. Kami menyediakan jadwal fleksibel termasuk akhir pekan sesuai ketersediaan.' },
	{ q: 'Bagaimana jika saya tidak puas?', a: 'Setiap pekerjaan mengikuti quality checklist. Jika ada yang tidak sesuai, hubungi kami dan kami akan menindaklanjutinya.' },
];