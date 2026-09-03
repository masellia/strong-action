FROM ruby:3.3-slim

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential git inotify-tools nodejs zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /srv/jekyll

COPY Gemfile Gemfile.lock ./
RUN gem install --no-document bundler && bundle install

COPY bin/entry_point.sh /usr/local/bin/entry_point
RUN chmod +x /usr/local/bin/entry_point

EXPOSE 8080 35729

CMD ["entry_point"]
