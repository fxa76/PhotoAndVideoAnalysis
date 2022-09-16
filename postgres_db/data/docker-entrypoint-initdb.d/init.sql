--
-- PostgreSQL database dump
--

-- Dumped from database version 12.10 (Debian 12.10-1.pgdg110+1)
-- Dumped by pg_dump version 12.10 (Debian 12.10-1.pgdg110+1)

--SET statement_timeout = 0;
--SET lock_timeout = 0;
--SET idle_in_transaction_session_timeout = 0;
--SET client_encoding = 'UTF8';
--SET standard_conforming_strings = on;
--SELECT pg_catalog.set_config('search_path', '', false);
--SET check_function_bodies = false;
--SET xmloption = content;
--SET client_min_messages = warning;
--SET row_security = off;

--
-- Name: calculate_all_faces_distances(); Type: FUNCTION; Schema: public; Owner: fxa_images_postgres_user
--

CREATE FUNCTION public.calculate_all_faces_distances() RETURNS void
    LANGUAGE plpgsql
    AS $$
declare
    f1 record;
    f2 record;
begin
    for f1 in select objects_id,face_encodings 
           from objects where face_encodings notnull 
    loop 
    	for f2 in select objects_id,face_encodings 
           from objects  where face_encodings notnull 
    	loop 
    		insert into face_distances (face_from,face_to,distance) values(f1.objects_id, f2.objects_id, distance(f1.face_encodings,f2.face_encodings) ) ;
    	end loop;
    end loop;
end;
$$;


ALTER FUNCTION public.calculate_all_faces_distances() OWNER TO fxa_images_postgres_user;

--
-- Name: distance(double precision[], double precision[]); Type: FUNCTION; Schema: public; Owner: fxa_images_postgres_user
--

CREATE FUNCTION public.distance(l double precision[], r double precision[]) RETURNS double precision
    LANGUAGE plpgsql
    AS $$
DECLARE
  s real;
BEGIN
  s := 0;
  FOR i IN 1..128 LOOP
    s := s + ((l[i] - r[i]) * (l[i] - r[i]));
  END LOOP;
 	
  RETURN |/ s;
END;
$$;


ALTER FUNCTION public.distance(l double precision[], r double precision[]) OWNER TO fxa_images_postgres_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: album_images_rel; Type: TABLE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE TABLE public.album_images_rel (
    album_id integer NOT NULL,
    image_id integer NOT NULL
);


ALTER TABLE public.album_images_rel OWNER TO fxa_images_postgres_user;

--
-- Name: albums_album_id_seq; Type: SEQUENCE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE SEQUENCE public.albums_album_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.albums_album_id_seq OWNER TO fxa_images_postgres_user;

--
-- Name: albums; Type: TABLE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE TABLE public.albums (
    album_id integer DEFAULT nextval('public.albums_album_id_seq'::regclass) NOT NULL,
    title character varying,
    comments character varying
);


ALTER TABLE public.albums OWNER TO fxa_images_postgres_user;

--
-- Name: analysis_analysis_id_seq; Type: SEQUENCE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE SEQUENCE public.analysis_analysis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.analysis_analysis_id_seq OWNER TO fxa_images_postgres_user;

--
-- Name: analysis; Type: TABLE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE TABLE public.analysis (
    analysis_id bigint DEFAULT nextval('public.analysis_analysis_id_seq'::regclass) NOT NULL,
    image_id integer NOT NULL,
    analyzer character varying NOT NULL,
    analyzer_version integer NOT NULL,
    started date,
    scheduled boolean NOT NULL,
    ended date
);


ALTER TABLE public.analysis OWNER TO fxa_images_postgres_user;

--
-- Name: face_distances; Type: TABLE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE TABLE public.face_distances (
    face_from bigint NOT NULL,
    face_to bigint NOT NULL,
    distance double precision NOT NULL
);


ALTER TABLE public.face_distances OWNER TO fxa_images_postgres_user;

--
-- Name: face_id; Type: TABLE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE TABLE public.face_id (
    face_id bigint NOT NULL,
    face_id_iteration bigint NOT NULL,
    hidden boolean
);


ALTER TABLE public.face_id OWNER TO fxa_images_postgres_user;

--
-- Name: images_image_id_seq; Type: SEQUENCE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE SEQUENCE public.images_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.images_image_id_seq OWNER TO fxa_images_postgres_user;

--
-- Name: images; Type: TABLE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE TABLE public.images (
    image_id integer DEFAULT nextval('public.images_image_id_seq'::regclass) NOT NULL,
    filefullname character varying(2303) NOT NULL,
    filename character varying(255) NOT NULL,
    filepath character varying(2048) NOT NULL,
    fileextensions character varying(10),
    filesize bigint,
    creationdate numeric,
    lat numeric,
    lon numeric,
    to_be_deleted boolean DEFAULT false NOT NULL,
    favorite boolean,
    coord_from_exif boolean,
    thumbnail character varying,
    source character varying(255),
    model character varying(255),
    duplicate_of_image_id bigint,
    othernames character varying[],
    comments character varying,
    "timestamp" timestamp without time zone,
    sha512 character varying(512) NOT NULL
);


ALTER TABLE public.images OWNER TO fxa_images_postgres_user;

--
-- Name: objects; Type: TABLE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE TABLE public.objects (
    objects_id integer NOT NULL,
    filefullname character varying(2303),
    bbox character varying(255),
    description character varying(255),
    confidence numeric,
    analyzer character varying(255) DEFAULT 'object_detector'::character varying NOT NULL,
    analyzer_version integer DEFAULT 100 NOT NULL,
    x integer,
    y integer,
    w integer,
    h integer,
    image_id integer,
    derived_from_object integer,
    object_image_filename character varying(2023),
    face_encodings double precision[],
    face_id integer,
    face_id_iteration integer,
    text_found character varying COLLATE pg_catalog."C.UTF-8"
);


ALTER TABLE public.objects OWNER TO fxa_images_postgres_user;

--
-- Name: objects_in_image_objects_id_seq; Type: SEQUENCE; Schema: public; Owner: fxa_images_postgres_user
--

CREATE SEQUENCE public.objects_in_image_objects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.objects_in_image_objects_id_seq OWNER TO fxa_images_postgres_user;

--
-- Name: objects_in_image_objects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fxa_images_postgres_user
--

ALTER SEQUENCE public.objects_in_image_objects_id_seq OWNED BY public.objects.objects_id;


--
-- Name: objects objects_id; Type: DEFAULT; Schema: public; Owner: fxa_images_postgres_user
--

ALTER TABLE ONLY public.objects ALTER COLUMN objects_id SET DEFAULT nextval('public.objects_in_image_objects_id_seq'::regclass);


--
-- Name: albums albums_pk; Type: CONSTRAINT; Schema: public; Owner: fxa_images_postgres_user
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_pk PRIMARY KEY (album_id);


--
-- Name: images image_id_unique; Type: CONSTRAINT; Schema: public; Owner: fxa_images_postgres_user
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT image_id_unique UNIQUE (image_id);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: fxa_images_postgres_user
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (filefullname);


--
-- Name: objects objects_in_image_pkey; Type: CONSTRAINT; Schema: public; Owner: fxa_images_postgres_user
--

ALTER TABLE ONLY public.objects
    ADD CONSTRAINT objects_in_image_pkey PRIMARY KEY (objects_id);


--
-- Name: face_distances face_distances_fk; Type: FK CONSTRAINT; Schema: public; Owner: fxa_images_postgres_user
--

ALTER TABLE ONLY public.face_distances
    ADD CONSTRAINT face_distances_fk FOREIGN KEY (face_from) REFERENCES public.objects(objects_id);


--
-- Name: face_distances face_distances_fk_1; Type: FK CONSTRAINT; Schema: public; Owner: fxa_images_postgres_user
--

ALTER TABLE ONLY public.face_distances
    ADD CONSTRAINT face_distances_fk_1 FOREIGN KEY (face_to) REFERENCES public.objects(objects_id);


--
-- Name: objects objects_in_images; Type: FK CONSTRAINT; Schema: public; Owner: fxa_images_postgres_user
--

ALTER TABLE ONLY public.objects
    ADD CONSTRAINT objects_in_images FOREIGN KEY (objects_id) REFERENCES public.objects(objects_id);

GRANT ALL PRIVILEGES ON DATABASE postgres TO fxa_images_postgres_user;

--
-- PostgreSQL database dump complete
--

